import os

import appdirs
import requests
from .data import *
from diskcache import Cache
from thefuzz import fuzz, process


class RestCountriesAPI:
    BASE_URL = "https://restcountries.com/v3.1"

    # caching to make sure we don't poll API for every request
    # declaring outside init so that this cache is shared across instances of this class
    cache_dir = appdirs.user_cache_dir("restcountries")
    os.makedirs(cache_dir, exist_ok=True)
    cache = Cache(cache_dir)

    def __init__(self):
        self.update_countries_cache()
        self._make_country_iso2_to_names_map()

    def _make_country_iso2_to_names_map(self):
        """Map each country's ISO2 code to a set of possible names."""
        countries_data = self.cache.get("countries_data")
        if not countries_data:
            return
        self.country_iso2_to_names_map = {}
        for country in countries_data:
            iso2 = country["cca2"]
            all_names = set()
            all_names.add(country["name"]["common"].lower())
            all_names.add(country["name"].get("official", "").lower())
            all_names.update([name.lower() for name in country.get("altSpellings", []) if len(name) > 2])
            all_names.update(translation.get("common", "").lower() for translation in country["translations"].values())
            all_names.update(
                translation.get("official", "").lower() for translation in country["translations"].values()
            )
            self.country_iso2_to_names_map[iso2] = all_names

    def update_countries_cache(self):
        """Fetches all country data from the API and caches it, using ETag to check for changes."""
        headers = {}
        etag = self.cache.get("etag")

        if etag:
            headers["If-None-Match"] = etag

        response = requests.get(f"{self.BASE_URL}/all", headers=headers)

        if response.status_code == 304:
            print("Data has not changed since the last fetch. Using cached data...")
            return  # Data in cache is still up to date
        if response.status_code == 200:
            print("Updating cache as data changed on remote...")
            self.cache.set("etag", response.headers.get("ETag"))
            self.cache.set("countries_data", response.json())
        else:
            response.raise_for_status()

    def close_cache(self):
        """Close the cache properly."""
        self.cache.close()

    def _parse_country(self, data: dict) -> Country:
        """Parse JSON data into a Country data class instance."""
        return from_dict(Country, data)

    def fetch_country_by_name(self, name: str) -> Country:
        """Fetch a country by its common name using cached data."""
        countries_data = self.cache.get("countries_data")
        if countries_data:
            country_data = next(
                (
                    item
                    for item in countries_data
                    if item["name"]["common"].lower() == name.lower()
                    or item["name"]["official"].lower() == name.lower()
                ),
                None,
            )
            if country_data:
                return self._parse_country(country_data)
        raise ValueError("Country not found in cache")

    def fetch_country_by_cca2(self, cca2: str) -> Country:
        """Fetch a country by its ISO2 code using cached data."""
        countries_data = self.cache.get("countries_data")
        if countries_data:
            country_data = next((item for item in countries_data if item["cca2"] == cca2), None)
            if country_data:
                return self._parse_country(country_data)
        raise ValueError("Country not found in cache")

    def fetch_country_by_cca3(self, cca3: str) -> Country:
        """Fetch a country by its ISO3 code using cached data."""
        countries_data = self.cache.get("countries_data")
        if countries_data:
            country_data = next((item for item in countries_data if item["cca3"] == cca3), None)
            if country_data:
                return self._parse_country(country_data)
        raise ValueError("Country not found in cache")

    def search_countries(self, query: str) -> List[Country]:
        """Search for countries using both direct and fuzzy matching."""
        query = query.lower()
        countries_data = self.cache.get("countries_data")
        # Direct match
        for iso2, names in self.country_iso2_to_names_map.items():
            if query in names:
                country_data = next((item for item in countries_data if item["cca2"] == iso2), None)
                return [self._parse_country(country_data)] if country_data else []

        # Fuzzy match
        all_names = [item for sublist in self.country_iso2_to_names_map.values() for item in sublist]
        best_match, score = process.extractOne(query, all_names, scorer=fuzz.WRatio)
        if score > 80:
            for iso2, names in self.country_iso2_to_names_map.items():
                if best_match in names:
                    country_data = next((item for item in countries_data if item["cca2"] == iso2), None)
                    return [self._parse_country(country_data)] if country_data else []

        return []  # No match found
