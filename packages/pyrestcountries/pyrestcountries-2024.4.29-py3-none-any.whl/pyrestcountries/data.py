from dataclasses import dataclass, fields, is_dataclass
from typing import Dict, List, Optional, TypeVar, Type

T = TypeVar("T")


def from_dict(cls: Type[T], data: Dict) -> T:
    if not is_dataclass(cls):
        raise ValueError(f"{cls} is not a dataclass")
    if isinstance(data, dict):
        field_types = {f.name: f.type for f in fields(cls)}
        field_data = {}
        for field_name, field_type in field_types.items():
            if isinstance(field_type, type) and issubclass(field_type, list) and hasattr(field_type, "__origin__"):
                # Handle list types
                item_type = field_type.__args__[0]
                field_data[field_name] = [from_dict(item_type, item) for item in data.get(field_name, [])]
            elif isinstance(field_type, type) and issubclass(field_type, dict) and hasattr(field_type, "__origin__"):
                # Handle dict types
                key_type, value_type = field_type.__args__
                field_data[field_name] = {
                    from_dict(key_type, k): from_dict(value_type, v) for k, v in data.get(field_name, {}).items()
                }
            elif is_dataclass(field_type):
                # Handle nested dataclasses
                field_data[field_name] = from_dict(field_type, data.get(field_name, {}))
            else:
                # Handle basic types
                field_data[field_name] = data.get(field_name)
        return cls(**field_data)


@dataclass
class NativeName:
    official: str
    common: str


@dataclass
class Name:
    common: str
    official: str
    nativeName: Dict[str, NativeName]


@dataclass
class Currency:
    name: str
    symbol: str


@dataclass
class Idd:
    root: str
    suffixes: List[str]


@dataclass
class Demonyms:
    f: str
    m: str


@dataclass
class Translation:
    official: str
    common: str


@dataclass
class Maps:
    googleMaps: str
    openStreetMaps: str


@dataclass
class Gini:
    year: float


@dataclass
class Car:
    signs: List[str]
    side: str


@dataclass
class Flags:
    png: str
    svg: str
    alt: Optional[str] = None


@dataclass
class CoatOfArms:
    png: str
    svg: str


@dataclass
class Country:
    name: Name
    tld: List[str]
    cca2: str
    ccn3: str
    cca3: str
    cioc: str
    independent: bool
    status: str
    unMember: bool
    currencies: Dict[str, Currency]
    idd: Idd
    capital: List[str]
    altSpellings: List[str]
    region: str
    subregion: str
    languages: Dict[str, str]
    translations: Dict[str, Translation]
    latlng: List[float]
    landlocked: bool
    borders: List[str]
    area: float
    demonyms: Dict[str, Demonyms]
    flag: str
    maps: Maps
    population: int
    gini: Dict[str, float]
    fifa: str
    car: Car
    timezones: List[str]
    continents: List[str]
    flags: Flags
    coatOfArms: CoatOfArms
    startOfWeek: str
    capitalInfo: Dict[str, float]
    postalCode: Dict[str, str]
