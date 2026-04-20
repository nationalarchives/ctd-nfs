# TODO: split out Farm initialization attributes to new Form dataclass module

from dataclasses import dataclass, field, InitVar
import shelve

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
    id: str = field(default_factory=create_uuid_str) 
    
    def __post_init__(self, filename):
        self.name = filename.name
        self.image_number = filename.image_number


@dataclass
class Form:
    document_type: InitVar[FormType]
    images: list[ImageFile]
    
    def __post_init__(self, document_type):
        self.name = document_type.name


@dataclass
class Details:
    name: str
    address: str
    full_address: str = field(init=False)


@dataclass
class Farm:
    county: str
    parish: str
    primary_farm_number: str

    farm_name: str = field(init=False)   
    additional_farms: str = field(init=False)

    addressee: Details = field(init=False)
    farmer: Details = field(init=False)
    landowner: Details = field(init=False)

    acreage: str = field(init=False)
    OS_map_sheet: str = field(init=False)
    field_info_date: str = field(init=False)
    primary_record_date: str = field(init=False)

    forms: list[Form] = field(default_factory=list)
    warnings: dict[str, list[str]] | None = None   
    source_data: dict[str, list[Transcription]] = field(default_factory=initialise_forms_mapping)

    def __post_init__(self):
        self._county_code, *_ = self.county.split()
        self._parish_number, *_ = self.parish.split()

    def _get_catalogue_reference_stem(self) -> str:
        """
        Retrieve the catalogue reference and county & parish values - county & parish value will be add to primary farm number to create farm reference

        Args:
            county_code (str):  
            parish_number (str): 

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
        
        return reference_record['Catalogue ref']
        
    @property
    def iaid() -> str:
        return create_uuid_str()

    @property
    def catalogue_reference(self) -> str:
        """The full catalogue reference will be displayed in Discovery, and mirrors the catalogue taxonomy in the format: "MAF 32/<piece>/<parish number>/<farm number>"
       Each farm must have a unique catalogue reference.

        Returns:
            str: catalogue reference for the farm
        """
        _catalogue_reference = self._get_catalogue_reference_stem()

        return f"{_catalogue_reference}/{self.primary_farm_number}"

    @property
    def farm_reference(self) -> str:
        return f"{self._county_code}/{self._parish_number}/{self.primary_farm_number}"


    # TODO: add warning for multiple B496/EI forms

    