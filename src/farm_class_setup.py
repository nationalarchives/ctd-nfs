from dataclasses import dataclass, field
import re
import csv
from typing import ClassVar


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


def split_items(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]


def clean_csv_data(raw_csv_data: csv.DictReader) -> list[dict]:
    """Utility method to clean raw csv data by splitting fields with multiple entries and stripping whitespace."""
    cleaned_data = []
    for row in raw_csv_data:
        for key, value in row.items():
            if ";" in value:
                row[key] = split_items(value)
            else:
                row[key] = value.strip()
        cleaned_data.append(row)
    return cleaned_data


"""
Occupier, Owner and Farmer will be initialised with lists of the relevant components from each row for that farm.
"""
@dataclass
class Details:
    title: list[str] | str
    individual_name: list[str] | str
    group_names: list[str] | str
    address: list[str] | str


@dataclass
class Farm:
    all_farms: ClassVar[dict[str, "Farm"]] = {}
    total_unclassified_farms_per_county: ClassVar[dict[int]] = {}   
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
    addressee: Details
    owner: Details
    farmer: Details
    acreage: list[str] | str
    OS_map_sheet: list[str] | str
    field_info_date: list[str] | str
    primary_record_date: list[str] | str
    catalogue_reference: str
    farm_reference: str
    forms: dict[list] = field(default_factory=make_forms_mapping)
    warnings: dict[list] = field(default_factory=make_warnings_mapping)

    def __init__(self, cleaned_csv_data: dict):
        """catalogue_reference & forms will have special methods to assign values later"""
        # self.forms = assign_filenames_to_forms(stripped_data),
        self.county = cleaned_csv_data['county']
        if self.county not in Farm.total_unclassified_farms_per_county:
            Farm.total_unclassified_farms_per_county[self.county] = 0
        self.parish = cleaned_csv_data['parish']
        self.primary_farm_number = cleaned_csv_data['primary_farm_number']
        self.additional_farms = cleaned_csv_data['additional_farms']
        self.farm_name = cleaned_csv_data['farm_name']
        self.addressee = Details(
            title=cleaned_csv_data['addressee_title'],
            individual_name=cleaned_csv_data['addressee_individual_name'],
            group_names=cleaned_csv_data['addressee_group_names'],
            address=cleaned_csv_data['address'],
        )
        self.owner = Details(
            title=cleaned_csv_data['owner_title'],
            individual_name=cleaned_csv_data['owner_individual_name'],
            group_names=cleaned_csv_data['owner_group_names'],
            address=cleaned_csv_data['owner_address'],
        )
        self.farmer = Details(
            title=cleaned_csv_data['farmer_title'],
            individual_name=cleaned_csv_data['farmer_individual_name'],
            group_names=cleaned_csv_data['farmer_group_names'],
            address=cleaned_csv_data['farmer_address'],
        )
        self.acreage = cleaned_csv_data['acreage']
        self.OS_map_sheet = cleaned_csv_data['OS_map_sheet']
        self.field_info_date = cleaned_csv_data['field_info_date']
        self.primary_record_date = cleaned_csv_data['primary_record_date']

    def make_catalogue_reference(self, row_number: int, reference_values: dict) -> None:
        """
        The full catalogue reference will be displayed in Discovery, and mirrors the catalogue taxonomy in the format: "MAF 32/<piece>/<parish number>/<farm number>"
        Each farm must have a unique catalogue reference.
        If a farm does not have a primary_farm_number, a farm number starting with U will be created. Farm numbers must be unique within a parish

        Args:
            row_number (int): row number in the csv file for warning messages
            reference_values (dict): piece, parish number & document_type parsed from filename
        """        
        self.piece = reference_values['piece']
        self.parish_number = reference_values['parish_number']
        farm_is_unclassified: bool = self.primary_farm_number in ["", "*"]

        if farm_is_unclassified:
            Farm.total_unclassified_farms_per_county[self.county] += 1
            farm_value = f"U{Farm.total_unclassified_farms_per_county[self.county]}"

        else:
            farm_value = self.primary_farm_number

        if reference_values['document_type'] not in ["Other", "Cover"]:
            self.warnings['Reference Warnings'] = f"Row {row_number}: Note - type is {reference_values['document_type'].lower()} so no farm number specified"
            farm_value = reference_values['document_type']

        if reference_values['document_type'] == "Cover" and self.primary_farm_number:
            self.warnings['Reference Warnings'] = f"Row {row_number}: Error - Type is cover and farm number is specified"
            farm_value = reference_values['document_type']

        self.catalogue_reference = \
            f"MAF 32/" \
            f"{self.piece}/" \
            f"{self.parish_number}/" \
            f"{farm_value}"

    def make_farm_reference(self):
        """
        Create a unique farm reference using the county code, parish number and primary farm number
        """
        county_code = self.county.split()[0]
        self.farm_reference = f"{county_code}/{self.parish_number}/{self.primary_farm_number}"
