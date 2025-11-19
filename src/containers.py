from dataclasses import dataclass, field
import re


def make_forms_mapping() -> dict:
    """Create a mapping of form codes to empty lists for storing filenames."""
    return {
        'C51/SSY': [],
        'B496/EI': [],
        'C 47/SSY': [],
        'C 49/SSY': [],
        'SF': [],
        'SF C69/SSY': [],
        'Other': [],
        'Cover': []
    }


def make_warnings_mapping() -> dict:
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


"""
Occupier, Owner and Farmer will be initialised with lists of the relevant components from each row for that farm.
"""
@dataclass
class Occupier:
    addressee_title: list[str] | str
    addressee_individual_name: list[str] | str
    addressee_group_names: list[str] | str
    address: list[str] | str


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
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_name: list[str]
    occupier: Occupier
    owner: Owner
    farmer: Farmer
    acreage: list[str] | str
    OS_map_sheet: list[str] | str
    field_info_date: list[str] | str
    primary_record_date: list[str] | str
    catalogue_reference: str = "MAF 32/"
    forms: dict[list] = field(default_factory=make_forms_mapping)
    warnings: dict[list] = field(default_factory=make_warnings_mapping)

    def clean_value(self, field_value: str) -> list[str]:
        """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
        return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]

    def __init__(self, raw_farm_data: dict):
        stripped_data = {key: value for key, value in raw_farm_data.items()}
        """catalogue_reference & forms will have special methods to assign values later"""
        # self.catalogue_reference = make_catalogue_reference(stripped_data),
        # self.forms = assign_filenames_to_forms(stripped_data),
        self.county = stripped_data['county'],
        self.parish = stripped_data['parish'],
        self.primary_farm_number = stripped_data['primary_farm_number'],
        self.additional_farms = self.clean_value(stripped_data['additional_farms']),
        self.farm_name = self.clean_value(stripped_data['farm_name']),
        self.occupier = Occupier(
            addressee_title=stripped_data['addressee_title'],
            addressee_individual_name=stripped_data['addressee_individual_name'],
            addressee_group_names=self.clean_value(stripped_data['addressee_group_names']),
            address=stripped_data['address']
        ),
        self.owner = Details(
            title=stripped_data['owner_title'],
            individual_name=stripped_data['owner_individual_name'],
            group_names=self.clean_value(stripped_data['owner_group_names']),
            address=stripped_data['owner_address']
        ),
        self.farmer = Details(
            title=stripped_data['farmer_title'],
            individual_name=stripped_data['farmer_individual_name'],
            group_names=self.clean_value(stripped_data['farmer_group_names']),
            address=stripped_data['farmer_address']
        ),
        self.acreage = stripped_data['acreage'],
        self.OS_map_sheet = stripped_data['OS_map_sheet'],
        self.field_info_date = stripped_data['field_info_date'],
        self.primary_record_date = stripped_data['primary_record_date'],

