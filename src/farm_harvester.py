"""
farm_Publisher

This module runs the first stage of the ETL pipeline for the Farm Survey data analysis work. 
The pipeline starts with a csv file of all the transcribed forms for a single county, which is then collated & transformed into individual farms,
and finally output in proof file of the data for each farm that will appear in the catalogue. 
This file will be sent to the CTD team to for review and possible edit.
The data for each farm is also stored in a JSON format in a document store

The ETL stages in this module are:
Extract:
* extract and normalize the transcription csv files
Transform:
* convert each transcription csv row into a Transcription dataclass instance
* collate transcription instances by farm
* create farm instances using the transcription data
Load
* load the farm instances, farm ids and image ids into databases
* output the farms in an Excel file in a format which allows easy review by the CTD team
    
Returns:
    Excel file containing representations of the farm instances. The Excel will serve two purposes:
    1. allow easy review of the resolution of the names & addresses
    2. contain all the data required to create the JSONs for Discovery (this will be used by MAF32_Publisher.py)

Yields:
    the module adds the farm instances to a database (in version 2.01 this is pickled data) and two key-value stores
    1. Farm_IDs maps each farm's catalogue reference to its iaID & replicaID
    2. File_IDs maps each form image file name to its image id
"""
import csv
import dbm
import shelve
from collections.abc import Generator, Iterator
from pathlib import Path

from src._dataclasses.farm_combine import HarvestedFarm
from src._dataclasses.transcription_model import Transcription
from src._tools.constants import CSVEXCEL, PATH
from src._tools.helpers import TranscriptionDataError, create_uuid_str
from src._tools.logging_setup import create_logger
from src._tools.xlwriter import ExcelWriter
from src.harvester.farm_attributiser import set_farm_attributes
from src.harvester.transcription_checker import TranscriptionChecker
from src.harvester.transcriptions_processor import TranscriptionsProcessor
from src.preview_builder import create_html_preview

logger = create_logger("src._config", "logging.yaml")


def create_proof_file(farms_store: dict, county: str, input_file_name: str, test_mode: bool = False) -> tuple:
    """_summary_

    Arguments:
        farms_store -- _description_
        county -- _description_
        input_file_name -- _description_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})
    """    
    farms_in_proof_format = [
            farm.to_proof()
            for farm in farms_store.values()
        ]
            
    excel_data = [{
        'sheet_name': "Proof data",
        'row_data': farms_in_proof_format,
        'column_settings': CSVEXCEL.PROOF_COLUMNS,
    }]
    harvest_dir = PATH.HARVEST / "TEST" / f"{county}" if test_mode else PATH.HARVEST / f"{county}"
    harvest_dir.mkdir(exist_ok=True, parents=True)
  
    proof_file_name = harvest_dir / f"{input_file_name.replace('_HarvesterIN_', '_HarvesterOUT_')}.xlsx"
    xlwriter = ExcelWriter()
    xlwriter.write_excel(excel_data, proof_file_name)

    return (
        proof_file_name,
        [
            {
                header_name: row[index]
                for index, (header_name, _) in enumerate(CSVEXCEL.PROOF_COLUMNS)
            }
            for row in farms_in_proof_format
        ]
        )


def process_transcriptions_for_each_farm(farms_store: dict[str, dict[str, HarvestedFarm]]) -> dict[str, dict[str, HarvestedFarm]]:
    """_summary_

    Arguments:
        farms_store -- _description_

    Returns:
        _description_
    """    
    total_farms = len(farms_store)

    for index, farm in enumerate(farms_store.values(), start=1):

        transcriptions = [
            item
            for element in farm.source_data.values()
            for item in element
        ]
        processor = TranscriptionsProcessor(transcriptions)
        farm = set_farm_attributes(farm, processor.process_transcriptions())
        farms_store[farm.catalogue_reference] = farm
        logger.info(f"Processed {index: 5d} of {total_farms: 5d}: {farm.farm_reference} ({farm.catalogue_reference})")

    return farms_store


def write_farms_to_db(farms_store: dict[str, HarvestedFarm], county: str, test_mode: bool = False) -> None:
    """_summary_

    Arguments:
        farms_store -- _description_
        county -- _description_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})
    """    
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        farm_db[county] = farms_store.copy()


def read_farms_db(county: str, test_mode: bool = False) -> dict[str, HarvestedFarm]:
    """_summary_

    Arguments:
        county -- _description_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})

    Returns:
        _description_
    """    
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'r') as farm_db:
        farms_store = farm_db[county].copy()

    return farms_store


def collate_transcription_by_farm(candidate_farm: HarvestedFarm, transcription: Transcription, farms_store: dict, row_number: int) -> HarvestedFarm:
    """_summary_

    Arguments:
        candidate_farm -- _description_
        transcription -- _description_
        farms_store -- _description_

    Returns:
        _description_
    """    
    form_type = transcription.document_type.name
    if candidate_farm.catalogue_reference not in farms_store:
        candidate_farm.source_data[form_type].append(transcription)
        logger.info(f"NEW FARM {candidate_farm.farm_reference} ({candidate_farm.catalogue_reference}) created from transcription instance {row_number} (form {form_type})")
        return candidate_farm

    else:
        existing_farm = farms_store[candidate_farm.catalogue_reference]
        existing_farm.source_data[form_type].append(transcription)
        logger.info(f"{'='*8} {candidate_farm.farm_reference} ({candidate_farm.catalogue_reference}) updated {'.'*4} from transcription instance {row_number} (form {form_type})")
        return existing_farm


def initialise_farm(transcription: Transcription) -> HarvestedFarm:
    """_summary_

    Arguments:
        transcription -- _description_

    Returns:
        _description_
    """    
    candidate_farm = HarvestedFarm(transcription.county, transcription.parish, transcription.primary_farm_number)
    """NOTE
    The FARM_IDS db will be deleted after Rutland (RD) and Isle of Wight (IW) have been archived
    """
    if transcription.county.startswith(("RD", "IW")):
        with dbm.open(PATH.FARM_IDS, 'c') as farm_ids_db:
            db_ids = farm_ids_db.get(candidate_farm.catalogue_reference, "")
            if db_ids:
                db_ids = eval(db_ids.decode())
                candidate_farm.id = db_ids['id']
                candidate_farm.replica_id = db_ids['replica_id']
            else:
                farm_ids_db[candidate_farm.catalogue_reference] = f"{{'id': '{candidate_farm.id}', 'replica_id': '{create_uuid_str()}'}}"

    return candidate_farm


def transform_row_to_transcription(farm_data_row: dict, row_number: int) -> Transcription | None:
    """_summary_

    Arguments:
        farm_data_row -- _description_
        row_number -- _description_

    Returns:
        _description_
    """    
    try:
        transcription = Transcription(**farm_data_row)
        if transcription.trid.value in Transcription.all_ids:
            raise TranscriptionDataError(f"ID {transcription.trid.value} is duplicated - each row must have a unique ID value")
        else:
            Transcription.all_ids.add(transcription.trid.value)

        if transcription.is_cover_page:
            msg = f"Row {row_number} is a cover so will not be processed."
            logger.info(f"{'!'*17} {msg}")
            return

        checker = TranscriptionChecker(transcription, row_number)
        transcription.warnings = checker.run_validation_checks()
        return transcription

    except TranscriptionDataError as error_message:
        logger.error(f"Row {row_number} not processed because {error_message}")
        return


def transform_row_data_to_farms(csv_data: Iterator[dict]) -> dict[str, dict[str, HarvestedFarm]]:
    """_summary_

    Arguments:
        csv_data -- _description_

    Returns:
        _description_
    """    
    """ rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row """
    initialised_farms = {}   
    for row_number, farm_data_row in enumerate(csv_data, start=2):
        if not (transcription := transform_row_to_transcription(farm_data_row, row_number)):
            continue

        candidate_farm = initialise_farm(transcription)
        candidate_farm = collate_transcription_by_farm(candidate_farm, transcription, initialised_farms, row_number)
        initialised_farms[candidate_farm.catalogue_reference] = candidate_farm

    return initialised_farms
        

def normalise_csv_data(raw_csv_data: Iterator[dict]) -> Generator[dict]:
    """_summary_

    Arguments:
        raw_csv_data -- _description_

    Yields:
        _description_
    """    
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
                normalised_data_row[key] = "_null_"

            elif "*" in value:
                normalised_data_row[key] = value.replace("*", "_not transcribed_")

            else:
                normalised_data_row[key] = value.strip()

        yield normalised_data_row


def load_data_from_file(csv_file: Path) -> Generator[dict]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        Generator[dict, None, None]: _description_
    """

    try:
        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
            yield from raw_csv_data

    except csv.Error as csv_error_message:
        logger.info(f"!!! ERROR in data loading: {csv_error_message}")


def run_pipeline(test_mode: bool=False) -> None:
    """_summary_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})
    """    
    input_files = PATH.INPUT.glob("TEST/*MAF32_HarvesterIN_*.csv") if test_mode else PATH.INPUT.glob("*MAF32_HarvesterIN_*.csv")

    for csv_file in input_files:
        logger.info(f"*** HARVESTING FILE: {csv_file.stem} ***")
        county, _ = csv_file.stem.split("_", maxsplit=1)
        raw_farm_data: Iterator[dict] = load_data_from_file(csv_file)
        normalised_farm_data: Iterator[dict] = normalise_csv_data(raw_farm_data)
        farms_store: dict = transform_row_data_to_farms(normalised_farm_data)
        write_farms_to_db(farms_store, county, test_mode)
        """ read from farm store - 
        this means that can comment out the loading and creation steps of the orchestration
        when only running Harvester to view changes to the proof output
        """
        farms_store = read_farms_db(county, test_mode)
        logger.info(f"*** PROCESSING TRANSCRIPTIONS for {county} ***")
        farms_store = process_transcriptions_for_each_farm(farms_store)
        write_farms_to_db(farms_store, county, test_mode)

        logger.info("*** CREATING PROOF FILE ***")
        proof_file, preview_data = create_proof_file(farms_store, county, csv_file.stem, test_mode)

        logger.info("*** CREATING HTML PREVIEW ***")
        create_html_preview(proof_file.stem, excel_data=preview_data)


if __name__ == "__main__":
    run_pipeline(test_mode=True)

