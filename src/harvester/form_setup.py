from dataclasses import dataclass
import re

from src._tools.helpers import DomainRuleValidationException, ValueObject
from src._tools.constants import REGEX, DATA


type ListOrStr = list[str] | str


def page_pattern_match(filename: str) -> re.Match:
    return REGEX.FORM_PATTERN.match(filename)


def cover_pattern_match(filename: str) -> re.Match:
    return REGEX.COVER_PATTERN.match(filename)


@dataclass(frozen=True)
class Filename(ValueObject):
    name: str

    def __post_init__(self):
        if not (page_pattern_match(self.name) or cover_pattern_match(self.name)):
            raise DomainRuleValidationException(f"{self.name} does not match expected pattern for form images or cover.")

    @property   
    def is_cover(self) -> bool:
        if cover_pattern_match(self.name) or page_pattern_match(self.name)['image_number'] == "0001":
            return True

        return False
    
    @property
    def image_number(self) -> int | None:
        if match := page_pattern_match(self.name):
            return int(match['image_number'])
    
    @property
    def piece(self) -> str:
        match = (page_pattern_match(self.name) or cover_pattern_match(self.name))
        return match['piece']
    
    @property
    def parish_number(self) -> str:
        match = (page_pattern_match(self.name) or cover_pattern_match(self.name))
        return match['parish_number']


@dataclass(frozen=True)
class FormType(ValueObject):
    name: str

    def __post_init__(self):
        if self.name not in DATA.FORM_TYPES:
            raise DomainRuleValidationException(f"Form type '{self.name}' is not a recognised form.")


@dataclass
class Form:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    filename_1: Filename
    filename_2: Filename | None
    document_type: FormType
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_name: list[str]
    addressee_title: ListOrStr
    addressee_individual_name: ListOrStr
    addressee_group_names: ListOrStr
    address: ListOrStr
    owner_title: ListOrStr
    owner_individual_name: ListOrStr
    owner_group_names: ListOrStr
    owner_address: ListOrStr
    farmer_title: ListOrStr
    farmer_individual_name: ListOrStr
    farmer_group_names: ListOrStr
    farmer_address: ListOrStr    
    acreage: ListOrStr
    OS_map_sheet: ListOrStr
    field_info_date: ListOrStr
    primary_record_date: ListOrStr

