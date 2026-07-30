# TODO: split out Farm initialization attributes to new Form dataclass module

from dataclasses import dataclass, field, InitVar
import shelve
import uuid
from functools import cached_property

from src._tools.constants import PATH
from src._tools.helpers import create_uuid_str
from src._dataclasses.transcription_model import Transcription, Filename


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


ImageSet = list[ImageFile]


@dataclass
class PostalDetails:
    name: str = ""
    address: str = ""
    
    @property
    def name_and_address(self) -> str:
        has_address = self.address != "[not specified]"
        has_name = self.name != "[not specified]"

        if (has_name and has_address):
            return f"{self.name}, {self.address}"
        
        if has_name and not has_address:
            return self.name

        if not has_name and has_address:
            return self.address
        
        if not (has_name or has_address):
            return "[not specified]"


@dataclass
class Respondent:
    details: list[PostalDetails]

    @property
    def names(self) -> list[str]:
        return [detail.name for detail in self.details]

    @property
    def addresses(self) -> list[str]:
        return [detail.address for detail in self.details]

    @property
    def names_and_addresses(self) -> list[str]:
        final = [
            detail.name_and_address
            for detail in self.details
            if detail.name_and_address != "[not specified]"
            ]
        return final if final else ["[not specified]",]


@dataclass
class Farm:
    county: str
    parish: str
    primary_farm_number: str

    farm_name: list[str] = field(init=False)   
    addressee: Respondent = field(init=False)
    farmer: Respondent = field(init=False)
    landowner: Respondent = field(init=False)

    acreage: list[str] = field(init=False)
    OS_map_sheet: list[str] = field(init=False)
    field_info_date: list[str] = field(init=False)
    primary_record_date: list[str] = field(init=False)

    _id: uuid.UUID = field(default_factory=create_uuid_str)
    _replica_id: uuid.UUID = field(default_factory=create_uuid_str)
    forms: dict[str, list[ImageSet]] = field(default_factory=dict)
    warnings: dict[str, list[str]] | None = None   
    source_data: dict[str, list[Transcription]] = field(default_factory=initialise_forms_mapping)

    def __post_init__(self):
        self._county_code, *_ = self.county.split()
        self._parish_number, *_ = self.parish.split()

    @property
    def id(self) -> str:
       return self._id
    
    @id.setter
    def id(self, value: uuid.UUID):
        self._id = value

    @property
    def replica_id(self) -> str:
       return self._replica_id
    
    @replica_id.setter
    def replica_id(self, value: uuid.UUID):
        self._replica_id = value

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

    def _process_forms_for_proof(self) -> dict:
        forms_in_proof_format = []
        files_in_proof_format = []
        ids_in_proof_format = []

        for form_type, images in self.forms.items():
            if len(images) == 1:
                forms_in_proof_format.append(form_type)
            else:
                for index in range(len(images)):
                    forms_in_proof_format.append(f"{form_type} ({index + 1})")
            for imageset in images:
                files_in_proof_format.append(", ".join([image.name for image in imageset]))
                ids_in_proof_format.append(", ".join([image.id for image in imageset]))

        return {
            'forms': forms_in_proof_format,
            'file_names': files_in_proof_format,
            'file_ids': ids_in_proof_format,
        }
            
    @staticmethod
    def _join(values: list, newline=True) -> str:
        if newline:
            _ = ";\n".join(values)
            return ";\n".join(_.split("; "))
        return "; ".join(values)

    def to_proof(self) -> list:
        forms_and_files = self._process_forms_for_proof()
        return [
            self.catalogue_reference,
            self._join(self.warnings.get('Reference Warnings', "")),
            self.id,
            # ========================
            self.replica_id,
            self._join(forms_and_files['file_ids']),
            self._join(forms_and_files['file_names']),
            self._join(self.warnings.get('Filename Warnings', "")),
            # ========================
            self._join(forms_and_files['forms']),
            self._join(self.warnings.get('Type Warnings', "")),
            self.farm_reference,
            self._join(self.farm_name),
            # ========================
            self._join(self.addressee.names),
            self.warnings.get('Addressee name warnings', ""),
            self._join(self.addressee.addresses),
            self._join(self.addressee.names_and_addresses),
            # ========================
            self._join(self.farmer.names),
            self.warnings.get('Farmer name warnings', ""),
            self._join(self.farmer.addresses),
            self._join(self.farmer.names_and_addresses),
            # ========================
            self._join(self.landowner.names),
            self.warnings.get('Landowner name warnings', ""),
            self._join(self.landowner.addresses),
            self._join(self.landowner.names_and_addresses),
            # ========================
            self._join(self.acreage),
            self._join(self.OS_map_sheet),
            self._join(self.field_info_date),
            self._join(self.primary_record_date),
        ]

