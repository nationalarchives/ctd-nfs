from dataclasses import dataclass, field
from collections import OrderedDict
import shelve

from src._config.constants import DATA


def concatenate_values(existing_value: list[str] | str, new_value: list[str] | str) -> list[str] | str:
    """Concatenate two values, ensuring no duplicates.

    Args:
        existing_value (list[str] | str): The existing value.
        new_value (list[str] | str): The new value to be added.

    Returns:
        list[str] | str: The concatenated value with duplicates removed.
    """
    if existing_value == new_value:
        return existing_value
    
    if new_value in ["", "*"]:
        return existing_value
    
    if existing_value in ["", "*"]:
        return new_value
    
    if type(existing_value) is str and type(new_value) is str:
        return [existing_value, new_value]

    if type(existing_value) is str and type(new_value) is list:
        for item in new_value:
            if item == existing_value:
                return new_value
        return [existing_value] + new_value

    if type(existing_value) is list and type(new_value) is str:
        for item in existing_value:
            if item == new_value:
                return existing_value
        return existing_value + [new_value]
    
    if type(existing_value) is list and type(new_value) is list:
        combined_list = existing_value.copy()
        for item in new_value:
            if item not in combined_list:
                combined_list.append(item)
        return combined_list


def concatenate_farms(existing_farm: 'Farm', new_farm: 'Farm') -> 'Farm':
    """Concatenate the forms, warnings, and source data of two Farm instances.

    Args:
        existing_farm (Farm): The existing Farm instance in the database.
        new_farm (Farm): The new Farm instance to be merged.

    Returns:
        Farm: The updated existing Farm instance with merged data.
    """
    # Merge forms
    for form_code, filenames in new_farm.forms.items():
        existing_farm.forms[form_code].extend(filenames)

    # Merge warnings
    for warning_category, warnings in new_farm.warnings.items():
        existing_farm.warnings[warning_category].extend(warnings)

    # Merge source data
    existing_farm.source_data.extend(new_farm.source_data)

    return existing_farm

def get_references(county_code: str, parish_number: str) -> tuple:
    """
    Retrieve the catalogue reference and county & parish values - county & parish value will be add to primary farm number to create farm reference

    Args:
        county_code (str):  
        parish_number (str): 

    Returns:
        tuple: 
    """ 
    with shelve.open(DATA.PIECE_LOOKUP_TABLE, "r") as piece_lookup_db:   
        all_references = (
            reference
            for reference in piece_lookup_db['pieces lookup table']
            if reference['County & Parish'] == f"{county_code}/{parish_number}"
        )
    reference_record = next(all_references, None)
    
    return (reference_record['Catalogue ref'], reference_record['County & Parish'])


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


def initialise_warnings_mapping() -> dict:
    """Create a mapping of warning categories to empty lists for storing warnings in the output file"""
    return {
        'Reference Warnings': [],
		'Filename Warnings': [],
		'Type Warnings': [],
		'Farm Number Warnings': [],
		'Farm Name Warnings': [],
		'Landowner Warnings': [],
		'Farmer Warnings': [],
		'Acreage Warnings': [],
		'Field Date Warnings': [],
		'Primary Date Warnings': []
    }


@dataclass
class Details:
    title: list[str] | str
    individual_name: list[str] | str
    group_names: list[str] | str
    address: list[str] | str


@dataclass
class Farm:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    filename_1: str
    filename_2: str
    document_type: str
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_name: list[str]
    addressee_title: list[str] | str
    addressee_individual_name: list[str] | str
    addressee_group_names: list[str] | str
    address: list[str] | str
    owner_title: list[str] | str
    owner_individual_name: list[str] | str
    owner_group_names: list[str] | str
    owner_address: list[str] | str
    farmer_title: list[str] | str
    farmer_individual_name: list[str] | str
    farmer_group_names: list[str] | str
    farmer_address: list[str] | str
    acreage: list[str] | str
    OS_map_sheet: list[str] | str
    field_info_date: list[str] | str
    primary_record_date: list[str] | str

    catalogue_reference: str = ""
    farm_reference: str = ""
    forms: OrderedDict[str, list[str]] = field(default_factory=initialise_forms_mapping)
    warnings: dict[str, list[str]] = field(default_factory=initialise_warnings_mapping)
    source_data: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.addressee = Details(
            title=self.addressee_title,
            individual_name=self.addressee_individual_name,
            group_names=self.addressee_group_names,
            address=self.address,
        )
        self.owner = Details(
            title=self.owner_title,
            individual_name=self.owner_individual_name,
            group_names=self.owner_group_names,
            address=self.owner_address,
        )
        self.farmer = Details(
            title=self.farmer_title,
            individual_name=self.farmer_individual_name,
            group_names=self.farmer_group_names,
            address=self.farmer_address,
        )
        self.create_references()
        self.assign_filenames_to_forms(),

    def create_references(self) -> None:
        """ 
        The full catalogue reference will be displayed in Discovery, and mirrors the catalogue taxonomy in the format: "MAF 32/<piece>/<parish number>/<farm number>"
        Each farm must have a unique catalogue reference.
        Create both the catalogue reference and farm reference for the farm using values from the lookup table and primary farm number
        The catalogue reference is made up of the catalogue reference from the lookup table and the primary farm number
        The farm reference is made up of the county code, parish number and primary farm number
        """        
        county_code, _ = self.county.split()
        parish_number, *_ = self.parish.split()

        catalogue_reference, county_and_parish = get_references(county_code, parish_number)

        self.catalogue_reference = \
            f"{catalogue_reference}/" \
            f"{self.primary_farm_number}"

        self.farm_reference = \
            f"{county_and_parish}/" \
            f"{self.primary_farm_number}"

    def assign_filenames_to_forms(self):
        """_summary_

        Args:
            csv_data (dict): _description_
        """
        self.forms[self.document_type].append(self.filename_1)
        if self.filename_2:
            self.forms[self.document_type].append(self.filename_2)

