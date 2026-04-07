from dataclasses import dataclass, InitVar
import re

from src._tools.helpers import DomainRuleValidationException, ValueObject
from src._tools.constants import REGEX, DATA


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
    filename_1: InitVar[Filename]
    filename_2: InitVar[Filename | None]
    document_type: FormType
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_name: list[str]
    addressee_title: str
    addressee_individual_name: str
    addressee_group_names: str
    address: str
    owner_title: str
    owner_individual_name: str
    owner_group_names: str
    owner_address: str
    farmer_title: str
    farmer_individual_name: str
    farmer_group_names: str
    farmer_address: str    
    acreage: str
    OS_map_sheet: str
    field_info_date: str
    primary_record_date: str

    def __post_init__(self):
        self.file1 = self.filename_1
        self.file2 = self.filename_2
