from pathlib import Path
from typing import Generator, Iterator
import csv
import re
import shelve

from src.row_data_validator import validate_data, has_valid_reference_values, row_is_cover_form, has_cover_issues
from src._config.constants import PATH, REGEX, CSVEXCEL
from src.farm_builder import Farm, concatenate_instance, initialise_warnings_mapping
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value)]


def clean_csv_data(raw_csv_data: Iterator[dict]) -> Generator[dict, None, None]:
    """Utility method to clean raw csv data by splitting fields with multiple entries and stripping whitespace."""
    for row in raw_csv_data:
        cleaned_data_row = {}
        for key, value in row.items():
            if key not in CSVEXCEL.CSV_HEADERS:
                continue
            if ";" in value:
                cleaned_data_row[key] = split_list_values(value)
            else:
                cleaned_data_row[key] = value.strip()
        
        yield cleaned_data_row


def load_data_from_file(csv_file: Path) -> Generator[dict, None, None]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        Generator[dict, None, None]: _description_
    """

    try:
        logger.info(f"Processing file: {csv_file.stem}")
        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
            for row in raw_csv_data:
                yield row
    
    except csv.Error as csv_error_message:
        logger.info(f"!!! ERROR in data loading: {csv_error_message}")


def update_farms_db(new_farm: Farm, row_data: dict, row_number: int, test_mode: bool = False) -> None:
    """_summary_
    """
    row_info = f"Processed row {row_number}:"
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        if new_farm.county not in farm_db:
            farm_db.update({new_farm.county: {}})

        county = farm_db[new_farm.county].copy()

        if new_farm.catalogue_reference not in farm_db[new_farm.county]:
            county[new_farm.catalogue_reference] = {'Farm': new_farm}
            county[new_farm.catalogue_reference]['source'] = [row_data,]
            logger.info(f"{row_info} NEW FARM: '{new_farm.catalogue_reference}' created from '{new_farm.document_type}'")

        else:
            existing_farm = county[new_farm.catalogue_reference]['Farm']
            county[new_farm.catalogue_reference]['Farm'] = concatenate_instance(existing_farm, new_farm)
            county[new_farm.catalogue_reference]['source'].append(row_data)
            logger.info(f"{row_info}{' '*50} '{new_farm.catalogue_reference}' {'.'*10} updated from '{new_farm.document_type}'")

        farm_db[new_farm.county] = county.copy()

def create_farms(csv_data: Iterator[dict], test_mode: bool = False) -> None:
    """ rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row """
    for row_number, farm_data_row in enumerate(csv_data, start=2):

        pattern_matches: dict[re.Match] = {
                'filename_1': REGEX.FORM_PATTERN.match(farm_data_row['filename_1']),
                'filename_2': REGEX.FORM_PATTERN.match(farm_data_row['filename_2']),
                'cover': REGEX.COVER_PATTERN.match(farm_data_row['filename_1']),
            }
        row_prefix = f"Row {row_number}: "
        warnings = initialise_warnings_mapping()

        if has_valid_reference_values(farm_data_row, pattern_matches, row_prefix) is False:
            continue
        
        if row_is_cover_form(farm_data_row['document_type'], pattern_matches): 
            warnings = has_cover_issues(farm_data_row, pattern_matches, row_prefix)
            if warnings is None:
                continue
        
        warnings = validate_data(farm_data_row, row_prefix, pattern_matches, warnings)

        candidate_farm = Farm(**farm_data_row)
        candidate_farm.warnings = warnings  
        update_farms_db(candidate_farm, farm_data_row, row_number, test_mode=test_mode)
        

def process_file(csv_file: Path, test_mode: bool = False) -> None:
    raw_farm_data: list[dict] = load_data_from_file(csv_file)
    cleaned_farm_data = clean_csv_data(raw_farm_data)
    create_farms(cleaned_farm_data, test_mode=test_mode)


if __name__ == "__main__":
    for csv_file in PATH.INPUT.glob("*.csv"):
        process_file(csv_file)

