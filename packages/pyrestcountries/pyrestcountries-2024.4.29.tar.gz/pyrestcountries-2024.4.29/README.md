# RestCountries

`RestCountries` is a Pythonic wrapper around the REST Countries API, which provides a simple way to access and use country data.

## Features

- Fetch information about countries using common name, ISO codes, etc.
- Cache responses locally to reduce API calls and increase performance.
- Simple and intuitive interface for accessing country data.

## Installation

Install `RestCountries` using pip:

```bash
pip install restcountries
```

## Usage

Here's a quick example to get you started:

```python
from restcountries import RestCountriesAPI

api = RestCountriesAPI()

# Fetch a country by common name
country = api.fetch_country_by_name("Finland")
print(country.name.common, country.capital)

# Get all countries data
api.update_countries_cache()
```

### Information available in Country Data Class

The `Country` data class encapsulates detailed information about a country. Here is what each attribute of the `Country` data class represents:

- **name**: An object containing the common and official names of the country along with native names in various local languages.

  - **common**: The commonly used name of the country.
  - **official**: The official name of the country.
  - **nativeName**: A dictionary with keys representing language codes and values providing names in those languages.

- **tld**: A list of top-level domains of the country.

- **cca2**: The two-letter country code as defined by ISO 3166-1 alpha-2.

- **ccn3**: The numeric country code as defined by ISO 3166-1 numeric.

- **cca3**: The three-letter country code as defined by ISO 3166-1 alpha-3.

- **cioc**: The International Olympic Committee country code.

- **independent**: Boolean value indicating whether the country is independent.

- **status**: General status of the country (e.g., "sovereign state").

- **unMember**: Boolean indicating whether the country is a member of the United Nations.

- **currencies**: A dictionary where keys are currency codes and values are objects containing name and symbol of each currency.

  - **name**: The name of the currency.
  - **symbol**: The symbol used for the currency.

- **idd**: An object representing international direct dialing information.

  - **root**: The IDD root.
  - **suffixes**: A list of IDD suffixes.

- **capital**: A list of names of the capital cities of the country.

- **altSpellings**: Alternative spellings of the country name.

- **region**: The region where the country is located (e.g., Europe, Asia).

- **subregion**: The subregion where the country is located.

- **languages**: A dictionary mapping language codes to names of languages spoken in the country.

- **translations**: A dictionary of translations of the country's name. Keys represent language codes, and values are objects containing translated names.

  - **official**: The official name of the country in the specified language.
  - **common**: The common name of the country in the specified language.

- **latlng**: A list containing the latitude and longitude of the country.

- **landlocked**: Boolean indicating whether the country is landlocked.

- **borders**: A list of country codes for countries that border the country.

- **area**: The total area of the country in square kilometers.

- **demonyms**: A dictionary with gender-specific demonyms for the country.

  - **f**: The feminine form of the demonym.
  - **m**: The masculine form of the demonym.

- **flag**: URL to the country's flag image.

- **maps**: An object containing URLs to maps of the country.

  - **googleMaps**: URL to the Google Maps location of the country.
  - **openStreetMaps**: URL to the OpenStreetMap location of the country.

- **population**: The total population of the country.

- **gini**: A dictionary where keys are years and values are the Gini coefficient for those years.

- **fifa**: The FIFA code for the country.

- **car**: An object containing information about car usage in the country.

  - **signs**: A list of car sign identifiers.
  - **side**: The side of the road vehicles drive on in the country.

- **timezones**: A list of all time zones applicable to the country.

- **continents**: A list of continents the country is part of.

- **flags**: An object containing URLs to images of the country's flag.

  - **png**: URL to a PNG image of the flag.
  - **svg**: URL to an SVG image of the flag.

- **coatOfArms**: An object containing URLs to images of the country's coat of arms.

  - **png**: URL to a PNG image of the coat of arms.
  - **svg**: URL to an SVG image of the coat of arms.

- **startOfWeek**: The day on which the week typically starts in the country.

- **capitalInfo**: A dictionary containing additional information about the capital.

  - **latlng**: Latitude and longitude of the capital.

- **postalCode**: A dictionary containing information about the postal code format.
  - **format**: The format of the postal code.
  - **regex**: A regular expression pattern that matches the postal code.

### API Methods

The `RestCountriesAPI` class provides several methods to retrieve and manipulate country data efficiently:

- **update_countries_cache()**: Fetches all country data from the Rest Countries API and caches it locally. Uses ETag headers to minimize unnecessary data transfer by checking if the data has changed since the last fetch.

- **fetch_country_by_name(name: str) -> Country**: Fetches detailed information about a country by its common or official name using the cached data. Returns a `Country` object if the country is found, otherwise raises a `ValueError`.

- **fetch_country_by_cca2(cca2: str) -> Country**: Retrieves country details by its ISO 3166-1 alpha-2 code. Returns a `Country` object if the country is found in the cache.

- **fetch_country_by_cca3(cca3: str) -> Country**: Retrieves country details by its ISO 3166-1 alpha-3 code. Similar to `fetch_country_by_cca2`, it returns a `Country` object if the country is available in the cached data.

- **search_countries(query: str) -> List[Country]**: Performs a search for countries using a query string. This method supports both direct matching and fuzzy matching across different locales to provide robust search capabilities. Returns a list of `Country` objects matching the query.

- **close_cache()**: Properly closes the cache used for storing country data. This should be called to ensure that all resources are cleanly released when the API object is no longer needed.

Each method is designed to handle data efficiently, leveraging local caching to reduce API calls and speed up response times for frequently requested data.

## Requirements

- Python 3.7+
- requests
- appdirs
- diskcache
- thefuzz

## Development

To set up a development environment:

1. Clone the repo:

   ```bash
   git clone https://github.com/gopalkoduri/restcountries.git
   cd restcountries
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## License

This project is licensed under the GNU Affero General Public License - see the [LICENSE](LICENSE) file for details.
