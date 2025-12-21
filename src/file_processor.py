from pathlib import Path
from typing import Generator, Iterator
import csv
import re

from constants import REGEX
from pre_instantiation_checks import validate_farm_reference_values


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
    for row_number, farm_data_row in enumerate(csv_data):
        print(f"\nProcessing row {row_number} ...")
        # Further processing logic would go here
        pattern_matches: dict[re.Match] = {
            'filename_1': REGEX.FORM_PATTERN.match(farm_data_row['filename_1']),
            'filename_2': REGEX.FORM_PATTERN.match(farm_data_row['filename_2']),
            'cover': REGEX.COVER_PATTERN.match(farm_data_row['filename_1']),
        }

        row_prefix = f"Row {farm_data_row['row_number']}: "

        if not validate_farm_reference_values(farm_data_row, pattern_matches, row_prefix):
            continue

    