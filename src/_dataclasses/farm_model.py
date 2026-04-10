# TODO: split out Farm initialization attributes to new Form dataclass module

from dataclasses import dataclass, field
from collections import OrderedDict
import shelve

from src._tools.constants import PATH, REGEX
from src._tools.helpers import create_uuid_str
from src._dataclasses.transcription_model import Filename, FormType


def initialise_forms_mapping() -> OrderedDict:
    """Create a mapping of form codes to empty lists for storing filenames.
        An orderedDict is used to maintain the order of forms as specified as there is a chronological significance to the order of forms.
        An enum was not used here as the form codes are not valid enum names .
    Returns:
        OrderedDict: Mapping of form codes to empty lists.
    """
    return OrderedDict([
        ('C 47/SSY', []),
        ('C 49/SSY', []),
        ('C51/SSY', []),
        ('SF', []),
        ('SF C69/SSY', []),
        ('B496/EI', []),
        ('Other', []),
        ('Cover', []),
    ])


def _get_catalogue_reference_stem(county_code: str, parish_number: str) -> str:
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
            if reference['County & Parish'] == f"{county_code}/{parish_number}"
        )
    reference_record = next(all_references, None)
    
    return reference_record['Catalogue ref']


@dataclass
class Image:
    name: str
    id: str = field(default_factory=create_uuid_str) 


@dataclass
class Form:
    images: list[Image]
    field_info_date: str
    primary_record_date: str


@dataclass
class Farm:
    file1: Filename
    file2: Filename
    form_type: FormType
    forms_to_files_map: OrderedDict[str, list[str]] = field(default_factory=initialise_forms_mapping)
    warnings: dict[str, list[str]]
        
    # TODO: change private variables to non-private - not necessary in property method as only return value will be available

    @property
    def iaid(self):
        return create_uuid_str()

    @property
    def catalogue_reference(self) -> str:
        """The full catalogue reference will be displayed in Discovery, and mirrors the catalogue taxonomy in the format: "MAF 32/<piece>/<parish number>/<farm number>"
       Each farm must have a unique catalogue reference.

        Returns:
            str: catalogue reference for the farm
        """
        _county_code, _ = self.county.split()
        _parish_number, *_ = self.parish.split()
        _catalogue_reference = _get_catalogue_reference_stem(_county_code, _parish_number)
        return f"{_catalogue_reference}/{self.primary_farm_number}"

    @property
    def farm_reference(self) -> str:
        _county_code, _ = self.county.split()
        _parish_number, *_ = self.parish.split()
        return f"{_county_code}/{_parish_number}/{self.primary_farm_number}"

    def assign_filenames_to_forms(self):
        """_summary_

        Args:
            csv_data (dict): _description_
        """
        new_images = [
            Image(file_name)
            for file_name in [self.filename_1, self.filename_2] 
            if file_name
        ]
        new_form = Form(
            images=new_images,
            field_info_date=self.field_info_date,
            primary_record_date=self.primary_record_date,
        )
        self.forms_to_files_map[self.document_type].append(new_form)

    def __post_init__(self):
    
        # TODO: move to new Farm dataclass
        self.assign_filenames_to_forms()


def concatenate_attribute_values(existing_value: str, new_value: str) -> str:
    """Concatenate two values, ensuring no duplicates.

    Args:
        existing_value (str): The existing value.
        new_value (str): The new value to be added.

    Returns:
        The concatenated value with duplicates removed.
    """
    if type(existing_value) is str and type(new_value) is str:
        return [existing_value, new_value]

    if type(existing_value) is str and type(new_value) is list:
        return [existing_value] + new_value

    if type(existing_value) is list and type(new_value) is str:
        return existing_value + [new_value]
    
    if type(existing_value) is list and type(new_value) is list:
        return existing_value + new_value


def concatenate_instance_attributes(existing_attribute: str, new_attribute: str, field_name: str) -> None:
    existing_value = getattr(existing_attribute, field_name)
    new_value = getattr(new_attribute, field_name)

    concatenated_value = concatenate_attribute_values(existing_value, new_value)
    setattr(existing_attribute, field_name, concatenated_value)


def is_consecutive_image(last_image: str, candidate_image: str) -> bool:
    image_number = int(REGEX.FORM_PATTERN.match(last_image)['image_number'])
    new_image_number = int(REGEX.FORM_PATTERN.match(candidate_image)['image_number'])
    return new_image_number == image_number + 1
           

def concatenate_forms(existing_forms: dict[str, Form], new_forms: dict[str, Form]) -> dict[str, Form]:
    for key in new_forms.keys():
        if not new_forms[key]:
            continue

        if not existing_forms[key]:
            existing_forms[key] = new_forms[key]
            continue

        current_last_image = existing_forms[key][0].images[-1].name
        new_image = new_forms[key][0].images[0].name
        if len(new_forms[key][0].images) == 1 and is_consecutive_image(current_last_image, new_image):
            existing_forms[key][0].images.append(new_image)
            concatenate_instance_attributes(existing_forms[key][0], new_forms[key][0], 'field_info_date')
            concatenate_instance_attributes(existing_forms[key][0], new_forms[key][0], 'primary_record_date')
        
        else:
            existing_forms[key].append(new_forms[key][0])

    return existing_forms 


def concatenate_instance(existing_farm: 'Farm', new_farm: 'Farm') -> 'Farm':
    """
    Concatenate the attributes of two Farm instances, ensuring no duplicates.

    Args:
        existing_farm (Farm): _description_
        new_farm (Farm): _description_

    Returns:
        Farm: _description_
    """        
    for field_name in existing_farm.__dict__:
        if field_name in ['addressee', 'owner', 'farmer']:
            existing_detail = getattr(existing_farm, field_name)
            new_detail = getattr(new_farm, field_name)       
            for detail_attribute in ['title', 'individual_name', 'group_names', 'address']:
                concatenate_instance_attributes(existing_detail, new_detail, detail_attribute)

        if field_name in ['additional_farms', 'farm_name', 'acreage', 'OS_map_sheet']:
            concatenate_instance_attributes(existing_farm, new_farm, field_name)

    existing_farm.forms_to_files_map = concatenate_forms(existing_farm.forms_to_files_map, new_farm.forms_to_files_map)

    # Merge warnings
    for warning_category, warnings in new_farm.warnings.items():
        existing_farm.warnings[warning_category].extend(warnings)

    return existing_farm



