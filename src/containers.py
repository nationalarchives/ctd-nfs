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

@dataclass
class Farm:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    catalogue_reference: str
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_names: list[str]
    # occupier details
    addressee_title: list[str] | str
    addressee_individual_name: list[str] | str
    addressee_group_names: list[str]
    address: list[str] | str
    # owner details
    owner_title: list[str] | str
    owner_individual_name: list[str] | str
    owner_group_names: list[str]
    owner_address: list[str] | str
    # farmer details
    farmer_title: list[str] | str
    farmer_individual_name: list[str] | str
    farmer_group_names: list[str]
    farmer_address: list[str] | str
    acreage: list[str] | str
    OS_map_sheet: list[str] | str
    field_info_date: list[str] | str
    primary_record_date: list[str] | str
    forms: dict[list] = field(default_factory=make_forms_mapping)

    def clean_value(self, field_value: str) -> list[str]:
        """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
        return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]


def create_farm(raw_farm_data: dict) -> Farm:
    stripped_data = {key: value for key, value in raw_farm_data.items()}
    return Farm(
        # catalogue_reference & forms will have special methods to assign value
        # catalogue_reference=make_catalogue_reference(stripped_data),
        # forms=assign_filenames_to_forms(stripped_data),
        county=stripped_data['county'],
        parish=stripped_data['parish'],
        primary_farm_number=stripped_data['primary_farm_number'],
        additional_farms=Farm().split_and_strip_value(stripped_data['additional_farms']),
        farm_names=Farm().split_and_strip_value(stripped_data['farm_names']),
        addressee_title=stripped_data['addressee_title'],
        addressee_individual_name=stripped_data['addressee_individual_name'],
        addressee_group_names=Farm().split_and_strip_value(stripped_data['addressee_group_names']),
        address=stripped_data['address'],
        owner_title=stripped_data['owner_title'],
        owner_individual_name=stripped_data['owner_individual_name'],
        owner_group_names=Farm().split_and_strip_value(stripped_data['owner_group_names']),
        owner_address=stripped_data['owner_address'],
        farmer_title=stripped_data['farmer_title'],
        farmer_individual_name=stripped_data['farmer_individual_name'],
        farmer_group_names=Farm().split_and_strip_value(stripped_data['farmer_group_names']),
        farmer_address=stripped_data['farmer_address'],
        acreage=stripped_data['acreage'],
        OS_map_sheet=stripped_data['OS_map_sheet'],
        field_info_date=stripped_data['field_info_date'],
        primary_record_date=stripped_data['primary_record_date'],
    )
