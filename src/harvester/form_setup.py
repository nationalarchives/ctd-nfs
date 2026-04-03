from dataclasses import dataclass
import re

from _tools.helpers import BusinessRuleValidationException, ValueObject
from src._tools.constants import REGEX


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
            raise BusinessRuleValidationException(f"{self.name} does not match expected pattern for form images or cover.")

    @property   
    def is_cover(self) -> bool:
        if cover_pattern_match(self.name) or page_pattern_match(self.name)['image'] == "0001":
            return True

        return False     


@dataclass
class Form:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    filename_1: str # TODO: create Filename ValueObject to include validation currently in row_data_validator.py
    filename_2: str
    document_type: str
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

