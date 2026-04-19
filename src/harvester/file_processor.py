from pathlib import Path
from typing import Generator, Iterator
import csv
import re
import shelve
import logging

from src._tools.constants import PATH, CSVEXCEL
from src._dataclasses.transcription_model import Transcription
from src._tools.helpers import TranscriptionDataError
from src.harvester.transcription_checker import TranscriptionChecker
from src._dataclasses.farm_model import Farm


logger = logging.getLogger(__name__)


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


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value) if item != "*"]


def normalise_csv_data(raw_csv_data: Iterator[dict]) -> Generator[dict, None, None]:
    """Utility method to normalise raw csv data by setting default values, splitting fields with multiple entries and stripping whitespace."""
    for row in raw_csv_data:
        normalised_data_row = {}
        for key, value in row.items():
            if key not in CSVEXCEL.CSV_HEADERS:
                continue
            
            if key == "filename_2" and value == "":
                normalised_data_row[key] = None
                continue
            
            if value == "":
                normalised_data_row[key] = "[not specified]"
            
            elif "*" in value:
                normalised_data_row[key] = value.replace("*", "[not specified]")
            
            else:
                normalised_data_row[key] = value.strip()
        
        yield normalised_data_row


def update_farms_db(transcription: Transcription, row_number: int, test_mode: bool = False) -> None:
    # NOTE: THIS IS INEFFICIENT BECAUSE IT COPIES THE WHOLE COUNTY FOR EACH TRANSCRIPTION
    # TODO: FIX THIS BY SWITCHING TO TINY DB AND JUST CREATING OR UPSERTING INDIVIDUAL FARMS
    # TODO: Initialise the db with all the counties
    row_info = f"Processed row {row_number}:"
    candidate_farm = Farm(transcription.county, transcription.parish, transcription.primary_farm_number)
    form_type = transcription.document_type.name

    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        if candidate_farm.county not in farm_db:
            farm_db.update({candidate_farm.county: {}})

        county = farm_db[candidate_farm.county].copy()

        if candidate_farm.catalogue_reference not in farm_db[candidate_farm.county]:
            candidate_farm.source_data[form_type].append(transcription)
            county[candidate_farm.catalogue_reference] = {'Farm': candidate_farm}
            logger.info(f"{row_info} NEW FARM: '{candidate_farm.catalogue_reference}' created from '{form_type}'")

        else:
            existing_farm = county[candidate_farm.catalogue_reference]['Farm']
            existing_farm.source_data[form_type].append(transcription)
            county[candidate_farm.catalogue_reference]['Farm'] = existing_farm
            logger.info(f"{row_info}{' '*50} '{candidate_farm.catalogue_reference}' {'.'*10} updated from '{form_type}'")

        farm_db[candidate_farm.county] = county.copy()


def create_farms(csv_data: Iterator[dict], test_mode: bool = False) -> None:
    """ rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row """
    for row_number, farm_data_row in enumerate(csv_data, start=2):
        try: 
            transcription = Transcription(**farm_data_row)
            if transcription.is_cover_page:
                msg = f"Row {row_number} is a cover so will not be processed."
                logger.info(f" {msg:->80}")
                continue
        
            checker = TranscriptionChecker(transcription, row_number)
            transcription.warnings = checker.run_validation_checks()
            update_farms_db(transcription, row_number, test_mode=test_mode)
        
        except TranscriptionDataError as error_message:
            logging.error(f"Row {row_number} not processed because {error_message}")
            continue

       
def process_csv_files(test_mode: bool = False) -> None:
    input_files = PATH.TEST_INPUT.glob("*.csv") if test_mode else PATH.INPUT.glob("*.csv")
    for csv_file in input_files:
        raw_farm_data: list[dict] = load_data_from_file(csv_file)
        normalised_farm_data = normalise_csv_data(raw_farm_data)
        create_farms(normalised_farm_data, test_mode=test_mode)

