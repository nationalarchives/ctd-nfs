from dataclasses import dataclass
import re
import csv
from typing import ClassVar
from collections import OrderedDict

from src.constants import DATA


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


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]


def clean_csv_data(raw_csv_data: csv.DictReader) -> list[dict]:
    """Utility method to clean raw csv data by splitting fields with multiple entries and stripping whitespace."""
    cleaned_data = []
    for row in raw_csv_data:
        for key, value in row.items():
            if ";" in value:
                row[key] = split_list_values(value)
            else:
                row[key] = value.strip()
        cleaned_data.append(row)
    return cleaned_data


def get_references(county_code: str, parish_number: str) -> tuple:
    """
    Retrieve the catalogue reference and county & parish values - county & parish value will be add to primary farm number to create farm reference

    Args:
        county_code (str):  
        parish_number (str): 

    Returns:
        tuple: 
    """    
    all_references = (
        reference
        for reference in DATA.LOOKUP_TABLE
        if reference['County & Parish'] == f"{county_code}/{parish_number}"
    )
    reference_record = next(all_references, None)
    
    return (reference_record['Catalogue ref'], reference_record['County & Parish'])


@dataclass
class Details:
    title: list[str] | str
    individual_name: list[str] | str
    group_names: list[str] | str
    address: list[str] | str


@dataclass
class Farm:
    all_farms: ClassVar[dict[str, "Farm"]] = {}
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
    catalogue_reference: str
    farm_reference: str
    forms: OrderedDict[str, list[str]]

    def __init__(self, cleaned_csv_data: dict):
        self.county = cleaned_csv_data['county']
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

        self.create_references()
        self.forms = initialise_forms_mapping()
        self.assign_filenames_to_forms(cleaned_csv_data['document_type'], cleaned_csv_data['filename_1'], cleaned_csv_data['filename_2']),
        self.warnings = {
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

    def assign_filenames_to_forms(self, document_type, filename_1, filename_2=None):
        """_summary_

        Args:
            csv_data (dict): _description_
        """
        self.forms[document_type].append(filename_1)
        if filename_2:
            self.forms[document_type].append(filename_2)
    
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

