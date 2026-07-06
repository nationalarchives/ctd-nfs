import csv
import shelve
from pathlib import Path
from typing import Generator, Iterator
import os
import dbm

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src._tools.logging_setup import create_logger
from src._tools.constants import CSVEXCEL, PATH
from src._tools.helpers import TranscriptionDataError, create_uuid_str
from src._tools.xlwriter import ExcelWriter
from src._dataclasses.farm_model import Farm
from src._dataclasses.transcription_model import Transcription
from src.harvester.transcription_checker import TranscriptionChecker
from src.harvester.transcriptions_processor import TranscriptionsProcessor
from src.harvester.farm_attributiser import set_farm_attributes


logger = create_logger("src._config", "logging.yaml")


def create_html_preview_page(farm_instances: Iterator, county: str) -> None:
    """This will build a WYSIWYG preview page of the description portion of the Discovery record for each farm in the county

    Arguments:
        farm_instances -- farm instances retrieved from the farms db
        county -- name of the county in format <CODE> <Name> e.g., "RD Rutland"
    """
    descriptions = [
        {
            'farm_reference': farm.farm_reference,
            'farm_name': farm.farm_name,
            'addressee': farm.addressee,
            'farmer': farm.farmer,
            'landowner': farm.landowner,
            'acreage': farm.acreage,
            'OS_map_sheet': farm.OS_map_sheet,
            'field_info_date': farm.field_info_date,
            'primary_record_date': farm.primary_record_date,
            'forms': farm.forms,
        }
        for farm in farm_instances
    ]
    
    farm_references = [
        farm.farm_reference
        for farm in farm_instances
    ]
    
    environment = Environment(
        loader=FileSystemLoader("src/_html/"), 
        autoescape=select_autoescape(enabled_extensions=('html', 'xml'), 
                                     default_for_string=True,)
        )
    previews_template = environment.get_template("farms_preview.html")
    previews_file = PATH.HARVEST / f"{county}_scopeAndContent previews.html"



def create_proof_files(farms_store: dict, county: str, input_file_name: str, test_mode: bool = False):
    proof_data = [
            farm.to_proof()
            for farm in farms_store.values()
        ]
            
    excel_data = [{
        'sheet_name': "Proof data",
        'row_data': proof_data,
        'column_settings': CSVEXCEL.PROOF_COLUMNS,
    }]
    
    proof_file_name = PATH.HARVEST / f"{input_file_name.replace('forHarvester', 'proof')}.xlsx"
    xlwriter = ExcelWriter()
    xlwriter.write_excel(excel_data, proof_file_name)


def update_farms(farms_store: dict[str, dict[str, Farm]], farms_to_update: list[tuple]) -> dict[str, dict[str, Farm]]:
    logger.info(" ===== COLLATING ATTRIBUTES FOR FARMS {county} ===== ")
   
    for index, (farm, farm_data) in enumerate(farms_to_update, start=1):
        farm = set_farm_attributes(farm, farm_data)

        farms_store[farm.catalogue_reference] = farm

        logger.info(f"Collating {index: 5d} for {farm.farm_reference}")

    return farms_store


def process_transcriptions_for_each_farm(farms_store: dict[str, dict[str, Farm]]) -> dict[str, dict[str, Farm]]:
    logger.info(" ===== PROCESSING TRANSCRIPTIONS for {county} ===== ")
    total_farms = len(farms_store)

    for index, farm in enumerate(farms_store.values(), start=1):

        logger.info(f"Processsing: '{farm.catalogue_reference}'")
        transcriptions = [
            item
            for element in farm.source_data.values()
            for item in element
        ]
        processor = TranscriptionsProcessor(transcriptions)
        farm = set_farm_attributes(farm, processor.process_transcriptions())
        farms_store[farm.catalogue_reference] = farm
        logger.info(f"Processed {index: 5d} of {total_farms: 5d}: {farm.farm_reference}")

    return farms_store


def write_farms_to_db(farms_store: dict[str, Farm], county: str, test_mode: bool = False) -> None:
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        farm_db[county] = farms_store.copy()


def read_farms_db(county: str, test_mode: bool = False) -> dict[str, Farm]:
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'r') as farm_db:
        farms_store = farm_db[county].copy()

    return farms_store


def collate_transcription_by_farm(candidate_farm: Farm, transcription: Transcription, farms_store: dict) -> Farm:
    form_type = transcription.document_type.name
    if candidate_farm.catalogue_reference not in farms_store:
        candidate_farm.source_data[form_type].append(transcription)
        logger.info(f"NEW FARM: '{candidate_farm.catalogue_reference}' {candidate_farm.id} created from '{form_type}'")
        return candidate_farm

    else:
        existing_farm = farms_store[candidate_farm.catalogue_reference]
        existing_farm.source_data[form_type].append(transcription)
        logger.info(f"{' '*50} '{candidate_farm.catalogue_reference}' {'.'*10} updated from '{form_type}'")
        return existing_farm


def initialise_farm(transcription: Transcription) -> Farm:
    candidate_farm = Farm(transcription.county, transcription.parish, transcription.primary_farm_number)
    with dbm.open(PATH.FARM_IDS, 'c') as farm_ids_db:
        db_ids = farm_ids_db.get(candidate_farm.catalogue_reference, "")
        if db_ids:
            db_ids = eval(db_ids.decode())
            candidate_farm.id = db_ids['id']
            candidate_farm.replica_id = db_ids['replica_id']
        else:
            farm_ids_db[candidate_farm.catalogue_reference] = "{'id': '%s', 'replica_id': '%s'}" % (candidate_farm.id, create_uuid_str())

    return candidate_farm


def transform_row_to_transcription(farm_data_row: dict, row_number: int) -> Transcription | None:
    try:
        transcription = Transcription(**farm_data_row)
        if transcription.is_cover_page:
            msg = f"Row {row_number} is a cover so will not be processed."
            logger.info(f" {msg:->80}")
            return

        checker = TranscriptionChecker(transcription, row_number)
        transcription.warnings = checker.run_validation_checks()
        logger.info(f"Transcription created from row {row_number}")
        return transcription

    except TranscriptionDataError as error_message:
        logger.error(f"Row {row_number} not processed because {error_message}")
        return


def transform_row_data_to_farms(csv_data: Iterator[dict]) -> dict[str, dict[str, Farm]]:
    """ rownumber is 1-indexed to match Excel row numbers, so start=2 to account for header row """
    logger.info(" ===== TRANSFORMING ROWS TO FARMS ===== ")
    initialised_farms = {}   
    for row_number, farm_data_row in enumerate(csv_data, start=2):
        if not (transcription := transform_row_to_transcription(farm_data_row, row_number)):
            continue

        candidate_farm = initialise_farm(transcription)
        candidate_farm = collate_transcription_by_farm(candidate_farm, transcription, initialised_farms)
        initialised_farms[candidate_farm.catalogue_reference] = candidate_farm

    return initialised_farms
        

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
                normalised_data_row[key] = "_null_"

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


def run_pipeline(test_mode: bool=False) -> None:
    input_files = PATH.TEST_INPUT.glob("*.csv") if test_mode else PATH.INPUT.glob("*.csv")
    logger.info(" ===== HARVESTING FARMS ===== ")

    for csv_file in input_files:
        county, _ = csv_file.stem.split("_", maxsplit=1)
        raw_farm_data: Iterator[dict] = load_data_from_file(csv_file)
        normalised_farm_data: Iterator[dict] = normalise_csv_data(raw_farm_data)
        farms_store: dict = transform_row_data_to_farms(normalised_farm_data)
        write_farms_to_db(farms_store, county, test_mode)
        """ read from farm store - 
        this means that can comment out the loading and creation steps of the orchestration
        when only running Harvester to view changes to the proof output
        """
        farms_store = read_farms_db(county)
        farms_store = process_transcriptions_for_each_farm(farms_store)
        write_farms_to_db(farms_store, county, test_mode)
        logger.info(" ===== CREATING PROOF FILES ===== ")
        create_proof_files(farms_store, county, csv_file.stem)


if __name__ == "__main__":
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    run_pipeline()

