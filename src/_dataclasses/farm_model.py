# TODO: split out Farm initialization attributes to new Form dataclass module

from dataclasses import dataclass, field, InitVar
import shelve
import uuid
from functools import cached_property

from src._tools.constants import PATH
from src._tools.helpers import create_uuid_str
from src._dataclasses.transcription_model import Transcription, Filename, FormType


def initialise_forms_mapping() -> dict:
    """Create a mapping of form codes to empty lists for storing filenames.
        The order of forms as specified is important as there is a chronological significance to the order of forms.
        An enum was not used here as the form codes are not valid enum names .
    Returns:
        dict: Mapping of form codes to empty lists.
    """
    return {
        'C 47/SSY': [],
        'C 49/SSY': [],
        'C51/SSY': [],
        'SF': [],
        'SF C69/SSY': [],
        'B496/EI': [],
        'Other': [],
        'Cover': [],
    }


@dataclass
class ImageFile:
    filename: InitVar[Filename]
    _id: uuid.UUID = field(default_factory=create_uuid_str) 
    
    def __post_init__(self, filename):
        self.name = filename.name
        self.image_number = filename.image_number

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: uuid.UUID):
        self._id = value


@dataclass
class Form:
    document_type: InitVar[FormType]
    images: list[ImageFile]
    
    def __post_init__(self, document_type):
        self.name = document_type.name


@dataclass
class Details:
    name: str = ""
    address: str = ""
    
    @property
    def full_address(self) -> str:
        has_address = self.address not in ["[not specified]", "_not transcribed_"]
        has_name = self.name not in ["[not specified]", "_not transcribed_"]

        if (has_name and has_address):
            return f"{self.name}, {self.address}"
        
        if has_name and not has_address:
            return self.name

        if not has_name and has_address:
            return self.address
        
        if not (has_name or has_address):
            return "[not specified]"


@dataclass
class Farm:
    county: str
    parish: str
    primary_farm_number: str

    farm_name: list[str] = field(init=False)   
    addressee: list[Details] = field(init=False)
    farmer: list[Details] = field(init=False)
    landowner: list[Details] = field(init=False)

    acreage: list[str] = field(init=False)
    OS_map_sheet: list[str] = field(init=False)
    field_info_date: list[str] = field(init=False)
    primary_record_date: list[str] = field(init=False)

    _id: uuid.UUID = field(default_factory=create_uuid_str)
    forms: list[Form] = field(default_factory=list)
    warnings: dict[str, list[str]] | None = None   
    source_data: dict[str, list[Transcription]] = field(default_factory=initialise_forms_mapping)

    def __post_init__(self):
        self._county_code, *_ = self.county.split()
        self._parish_number, *_ = self.parish.split()

    @cached_property
    def id(self) -> str:
       return self._id

    @cached_property
    def catalogue_reference(self) -> str:
        """
        Calculates the full catalogue reference by retrieving the partial catalogue reference corresponding to the county & parish values from a lookup table,
        and adding this to the primary farm number
        The full catalogue reference will be displayed in Discovery, and mirrors the catalogue taxonomy in the format: "MAF 32/<piece>/<parish number>/<farm number>"
        Each farm must have a unique catalogue reference.

        Returns:
        str: Catalogue reference stem e.g. "MAF 32/1/8" (full catalogue reference will be "MAF 32/1/8/<I>" where <I> is the primary farm number)
        """ 
        with shelve.open(PATH.PIECE_LOOKUP_TABLE, "r") as piece_lookup_db:   
            all_references = (
                reference
                for reference in piece_lookup_db['pieces lookup table']
                if reference['County & Parish'] == f"{self._county_code}/{self._parish_number}"
            )
        reference_record = next(all_references, None)
        
        return f"{reference_record['Catalogue ref']}/{self.primary_farm_number}"

    @cached_property
    def farm_reference(self) -> str:
        return f"{self._county_code}/{self._parish_number}/{self.primary_farm_number}"

    # TODO: add warning for multiple B496/EI forms

    