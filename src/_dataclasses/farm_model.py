# TODO: split out Farm initialization attributes to new Form dataclass module

from dataclasses import dataclass, field, InitVar
from collections import OrderedDict
import shelve
import re
from datetime import datetime

from src._tools.constants import PATH, REGEX, DATA
from src._tools.helpers import create_uuid_str
from src._dataclasses.transcription_model import Transcription


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


def _normalize_date(candi_date: str) -> str:
    """Normalize date strings to a standard format day month year format e.g. 1 January 1941.
    Note: day must not have leading zeros.

    Args:
        date_str (str): The date string to normalize.

    Returns:
        str: The normalized date string.
    """

    if REGEX.MONTH.match(candi_date) or REGEX.MON.match(candi_date):
        if REGEX.MON.match(candi_date):
            index = DATA.ABBR_MONTH_NAMES.index(candi_date)
            candi_date = DATA.MONTH_NAMES[index]
        return f"{candi_date}"

    if REGEX.DAYMONTH.match(candi_date) or REGEX.DAYMON.match(candi_date):
        day, month = candi_date.split()
        if REGEX.DAYMON.match(candi_date):
            index = DATA.ABBR_MONTH_NAMES.index(month)
            month = DATA.MONTH_NAMES[index]
        return f"{int(day)} {month}"

    candi_date = REGEX.REMOVE_DELIMITERS.sub(' ', candi_date)
    date_match: dict[re.Match] = {
        'daymonthyear': REGEX.DAYMONTHYEAR.match(candi_date),
        'ddmmyyyy': REGEX.DDMMYYYY.match(candi_date),
    }
    if not (date_match['daymonthyear'] or date_match['ddmmyyyy']):
        return candi_date
    
    for fmt in DATA.DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(candi_date, fmt)
            day, month, year = parsed_date.strftime("%d %B %Y").split()
            break
        except ValueError:
            continue

    return f"{int(day)} {month} {re.sub(r"^20", "19", year)}"


@dataclass
class Image:
    file: InitVar[Filename]
    id: str = field(default_factory=create_uuid_str)

    def __post_init__(self, file):
        self.name = file.name
        self.number = file.image_number


@dataclass
class Form:
    images: list[Image]
    field_info_date: str
    primary_record_date: str


@dataclass
class Details:
    name: str
    address: str


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

    warnings: dict[str, list[str]] | None = None   
    source_data: OrderedDict[str, list[Transcription]] = field(default_factory=initialise_forms_mapping)
        
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
            Image(image_file)
            for image_file in [self.filename_1, self.filename_2] 
            if image_file
        ]
        new_form = Form(
            images=new_images,
            field_info_date=self.field_info_date,
            primary_record_date=self.primary_record_date,
        )
        self.forms[self.document_type.name].append(new_form)


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
           

def concatenate_forms(existing_forms: dict[str, Form], new_forms: dict[str, Form]) -> dict[str, Form]:
    for key in new_forms.keys():
        if not new_forms[key]:
            continue

        if not existing_forms[key]:
            existing_forms[key] = new_forms[key]
            continue

        current_last_image = existing_forms[key][0].images[-1]
        new_image = new_forms[key][0].images[0]
        if len(new_forms[key][0].images) == 1 and (new_image.number == current_last_image.number + 1):
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

    existing_farm.forms = concatenate_forms(existing_farm.forms, new_farm.forms)

    # Merge warnings
    for warning_category, warnings in new_farm.warnings.items():
        existing_farm.warnings[warning_category].extend(warnings)

    return existing_farm



