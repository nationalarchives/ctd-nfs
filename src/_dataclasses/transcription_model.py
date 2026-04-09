from dataclasses import dataclass, InitVar
import re

from src._tools.helpers import TranscriptionDataError, ValueObject
from src._tools.constants import REGEX, DATA


def _page_pattern_match(filename: str) -> re.Match[str] | None:
    return REGEX.FORM_PATTERN.match(filename)


def _cover_pattern_match(filename: str) -> re.Match[str] | None:
    return REGEX.COVER_PATTERN.match(filename)


@dataclass(frozen=True)
class Filename(ValueObject):
    name: str

    def __post_init__(self):
        if not (_page_pattern_match(self.name) or _cover_pattern_match(self.name)):
            raise TranscriptionDataError(f"{self.name} does not match expected pattern for form images or cover.")

    @property   
    def is_cover(self) -> bool:
        if _cover_pattern_match(self.name):
            return True
        if (match := _page_pattern_match(self.name)) and match['image_number'] == "0001":
            return True
        return False
    
    @property
    def image_number(self) -> int | None:
        if match := _page_pattern_match(self.name):
            return int(match['image_number'])
    
    @property
    def piece(self) -> str | None:
        if match := (_page_pattern_match(self.name) or _cover_pattern_match(self.name)):
            return match['piece']
    
    @property
    def parish_number(self) -> str | None:
        if match := (_page_pattern_match(self.name) or _cover_pattern_match(self.name)):
            return match['parish_number']


@dataclass(frozen=True)
class FormType(ValueObject):
    name: str

    def __post_init__(self):
        if self.name not in DATA.FORM_TYPES:
            raise TranscriptionDataError(f"Form type '{self.name}' is not a recognised form.")


@dataclass
class Transcription:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    filename_1: InitVar[str]
    filename_2: InitVar[str | None]
    document_type: InitVar[str]
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: str
    farm_name: str
    addressee_title: InitVar[str]
    addressee_individual_name: InitVar[str]
    addressee_group_names: InitVar[str]
    address: InitVar[str]
    owner_title: InitVar[str]
    owner_individual_name: InitVar[str]
    owner_group_names: InitVar[str]
    owner_address: InitVar[str]
    farmer_title: InitVar[str]
    farmer_individual_name: InitVar[str]
    farmer_group_names: InitVar[str]
    farmer_address: InitVar[str]
    acreage: str
    OS_map_sheet: str
    field_info_date: str
    primary_record_date: str

    @property
    def no_data(self) -> bool:
        no_values = [
            getattr(self, field_name)
            for field_name in self.__dict__
            if field_name not in ['filename_1', 'filename_2','document_type', 'county', 'parish', ] \
                and getattr(self, field_name) == "[not specified]"
        ]
        return all(no_values)
    
    # @property
    # def is_cover_page(self) -> bool:
    #     if self.file1.cover and self.document_type == "Cover":
    #         return True
    #     return False
    
    def __post_init__(self, 
                      filename_1, filename_2, document_type):
        self.file1 = Filename(filename_1)
        self.file2 = Filename(filename_2) if filename_2 else None
        self.form_type = FormType(document_type)

        # if not self.is_cover_page and self.no_data:
        #     raise TranscriptionDataError(f"{self.file1.name} and {self.file2.name} have valid form patterns but no farm data provided.")

