from pathlib import Path
from typing import Generator, Iterator
import csv
import re

from constants import REGEX
from pre_instantiation_checks import \
    validate_farm_reference_values, \
    check_document_is_form_and_row_contains_farm_details, \
    check_values_between_filenames, \
    report_cover_image_inconsistencies
from farm_class_setup import Farm, initialise_warnings_mapping


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]


def clean_csv_data(raw_csv_data: Iterator[dict]) -> Generator[dict, None, None]:
    """Utility method to clean raw csv data by splitting fields with multiple entries and stripping whitespace."""
    cleaned_data = []
    for row in raw_csv_data:
        for key, value in row.items():
            if ";" in value:
                row[key] = split_list_values(value)
            else:
                row[key] = value.strip()
        cleaned_data.append(row)
    return iter(cleaned_data)


def load_data_from_file(csv_file: Path) -> Generator[dict, None, None]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        Generator[dict, None, None]: _description_
    """

    try:
        print(f"Processing file: {csv_file.stem}")
        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
        return iter(raw_csv_data)
    
    except csv.Error as csv_error_message:
        print(f"!!! ERROR in data loading: {csv_error_message}")


def process_csv_data(csv_data: Iterator[dict]) -> None:
    # rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row
    for row_number, farm_data_row in enumerate(csv_data, start=2):
        print(f"\nProcessing row {row_number} ...")
        # Further processing logic would go here
        pattern_matches: dict[re.Match] = {
            'filename_1': REGEX.FORM_PATTERN.match(farm_data_row['filename_1']),
            'filename_2': REGEX.FORM_PATTERN.match(farm_data_row['filename_2']),
            'cover': REGEX.COVER_PATTERN.match(farm_data_row['filename_1']),
        }

        row_prefix = f"Row {row_number}: "

        if not validate_farm_reference_values(farm_data_row, pattern_matches, row_prefix):
            continue

        if not check_document_is_form_and_row_contains_farm_details(farm_data_row, pattern_matches, row_prefix):
            continue

        warnings: dict = initialise_warnings_mapping()
        if pattern_matches['filename_1'] and pattern_matches['filename_2']:
            warnings = check_values_between_filenames(farm_data_row, pattern_matches, warnings, row_prefix)

        if farm_data_row['document_type'] == 'Cover' or pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001":
            warnings = report_cover_image_inconsistencies(farm_data_row, pattern_matches, warnings, row_prefix) 

        candidate_farm = Farm(**farm_data_row)
        candidate_farm.warnings = warnings
        if candidate_farm.catalogue_reference not in Farm.all_farms:
            Farm.all_farms[candidate_farm.catalogue_reference] = candidate_farm
            print(f"Successfully instantiated Farm: {candidate_farm.catalogue_reference}")
        else:
            print(f"Catalogue reference {candidate_farm.catalogue_reference} already exists. Merging data ...")


def process_file(csv_file: Path) -> None:
    raw_farm_data: list[dict] = load_data_from_file(csv_file)
    cleaned_farm_data = clean_csv_data(raw_farm_data)
    process_csv_data(cleaned_farm_data)