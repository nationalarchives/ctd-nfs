import csv
import shelve
from pathlib import Path
from typing import Generator, Iterator

from src._tools.logging_setup import create_logger
from src._tools.constants import CSVEXCEL, PATH
from src._tools.helpers import TranscriptionDataError
from src._dataclasses.farm_model import Farm
from src._dataclasses.transcription_model import Transcription
from src.harvester.transcription_checker import TranscriptionChecker
from src.harvester.transcriptions_processor import TranscriptionsProcessor
# from src.harvester.catalogue_proofs_builder import create_proof_files


logger = create_logger("src._config", "logging.yaml")


def process_transcriptions(county: str, test_mode: bool) -> None:
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        logger.info(" ===== PROCESSING FARMS ===== ")
        farms_in_county = farm_db[county].copy()
        total_farms = len(farms_in_county.values())

        for index, data in enumerate(farms_in_county.values(), start=1):
            farm = data['farm']
            transcriptions = [
                item
                for element in farm.source_data.values()
                for item in element
            ]
            processor = TranscriptionsProcessor(transcriptions)
            results = processor.process_transcriptions()

            farm.forms = results['forms']

            for field, value in results['for output'].items():
                setattr(farm, field, value)

            farms_in_county[farm.catalogue_reference]['farm'] = farm

            distilled_data = results['for_processing']

            logger.info(f"Processed {index: 5d} of {total_farms: 5d}: {farm.farm_reference}")
        farm_db[county] = farms_in_county.copy()


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
            county[candidate_farm.catalogue_reference] = {'farm': candidate_farm}
            logger.info(f"{row_info} NEW FARM: '{candidate_farm.catalogue_reference}' created from '{form_type}'")

        else:
            existing_farm = county[candidate_farm.catalogue_reference]['farm']
            existing_farm.source_data[form_type].append(transcription)
            county[candidate_farm.catalogue_reference]['farm'] = existing_farm
            logger.info(f"{row_info}{' '*50} '{candidate_farm.catalogue_reference}' {'.'*10} updated from '{form_type}'")

        farm_db[candidate_farm.county] = county.copy()


def create_farms(csv_data: Iterator[dict], test_mode: bool = False) -> None:
    """ rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row """
    logger.info(" ===== LOADING TRANSCRIPTIONS & CREATING FARMS ===== ")
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


def normalise_csv_data(raw_csv_data: Iterator[dict]) -> Generator[dict, None, None]:
    """Utility method to normalise raw csv data by setting default values, splitting fields with multiple entries and stripping whitespace."""
    logger.info(" ===== NORMALIZING CSV DATA ===== ")
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
                normalised_data_row[key] = value.replace("*", "_not transcribed_")

            else:
                normalised_data_row[key] = value.strip()

        yield normalised_data_row


def load_data_from_file(csv_file: Path) -> Generator[dict, None, None]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        Generator[dict, None, None]: _description_
    """

    try:
        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
            logger.info(f" ===== PROCESSING FILE: {csv_file.stem} ===== ")
            for row in raw_csv_data:
                yield row

    except csv.Error as csv_error_message:
        logger.info(f"!!! ERROR in data loading: {csv_error_message}")


def process_csv_files(test_mode: bool = False) -> None:
    input_files = PATH.TEST_INPUT.glob("*.csv") if test_mode else PATH.INPUT.glob("*.csv")
    for csv_file in input_files:
        raw_farm_data: list[dict] = load_data_from_file(csv_file)
        normalised_farm_data = normalise_csv_data(raw_farm_data)
        create_farms(normalised_farm_data, test_mode=test_mode)
    process_transcriptions('KT Kent', test_mode=test_mode)


def main():
    logger.info(" ===== HARVESTING FARMS ===== ")
    process_csv_files()

    # logger.info(" ===== CREATING PROOF FILES ===== ")
    # create_proof_files()


if __name__ == "__main__":
    main()

