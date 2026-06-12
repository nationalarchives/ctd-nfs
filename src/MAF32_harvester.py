import csv
import shelve
from pathlib import Path
from typing import Generator, Iterator
import os
import dbm
import re

from src._tools.logging_setup import create_logger
from src._tools.constants import CSVEXCEL, PATH
from src._tools.helpers import TranscriptionDataError, create_uuid_str
from src._dataclasses.farm_model import Farm, PostalDetails, Respondent
from src._dataclasses.transcription_model import Transcription
from src.harvester.transcription_checker import TranscriptionChecker
from src.harvester.transcriptions_processor import TranscriptionsProcessor
from src.harvester.details_resolver import resolve_postal_details
from src._tools.xlwriter import ExcelWriter


logger = create_logger("src._config", "logging.yaml")


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


def collate_attributes(values: list[str]) -> str:
    output = []
    for item in values:
        if item not in output and item not in ["_null_", "_not transcribed_"]:
            output.append(item)

    return output or ["[not specified]",]


def get_postal_details_warnings(addressee_warning: str, farmer_warning: str, landowner_warning: str) -> dict:
    farm_warnings = {}
    if addressee_warning:
        farm_warnings.update({'Addressee name warnings': addressee_warning})
    if farmer_warning:
        farm_warnings.update({'Farmer name warnings': farmer_warning})
    if landowner_warning:
        farm_warnings.update({'Landowner name warnings': landowner_warning})

    return farm_warnings


def create_respondents(farm: Farm, addressee_details: dict, farmer_details: dict, landowner_details: dict) -> Farm:
    farm.addressee = Respondent(set_postal_details(addressee_details))
    farm.farmer = Respondent(set_postal_details(farmer_details))
    farm.landowner = Respondent(set_postal_details(landowner_details))
    
    return farm


def set_postal_details(values: list[dict]) -> list[PostalDetails]:
    if len(values) > 1:
        final_values = [
            item
            for item in values
            if (item['name'], item['address']) != ('[not specified]', '[not specified]')
        ]
    else:
        final_values = values

    return [
        PostalDetails(name=item['name'], address=item['address'])
        for item in final_values
    ]


def resolve_postal_details_of_respondents(attributes: dict) -> dict:
    addressee_details, addressee_warning = resolve_postal_details(
            attributes['addressee_title'], 
            attributes['addressee_individual_name'], 
            attributes['addressee_group_names'], 
            attributes['address'],
        )
    landowner_details, landowner_warning = resolve_postal_details(
            attributes['owner_title'], 
            attributes['owner_individual_name'], 
            attributes['owner_group_names'], 
            attributes['owner_address'],
        )
    farmer_details, farmer_warning = resolve_postal_details(
            attributes['farmer_title'], 
            attributes['farmer_individual_name'], 
            attributes['farmer_group_names'],
            attributes['farmer_address'],
        )
    
    return {
        "details": {'addressee': addressee_details, 'farmer': farmer_details, 'landowner': landowner_details},
        "warnings": {'addressee': addressee_warning, 'farmer': farmer_warning, 'landowner': landowner_warning},
    }


def update_farms(farms_store: dict[str, dict[str, Farm]], farms_to_update: list[tuple]) -> dict[str, dict[str, Farm]]:
    logger.info(" ===== COLLATING ATTRIBUTES FOR FARMS {county} ===== ")
   
    for index, (farm, farm_data) in enumerate(farms_to_update, start=1):
        farm.forms = farm_data['forms']
        farm.field_info_date = farm_data['attributes']['field_info_date']
        farm.primary_record_date = farm_data['attributes']['primary_record_date']

        for field in ['farm_name', 'acreage', 'OS_map_sheet', 'field_info_date', 'primary_record_date']:
            value = farm_data['attributes'][field]
            output_value = collate_attributes(value)
            setattr(farm, field, output_value)

        unique_farm_names = []
        for names in farm.farm_name:
            for _name in re.split("; *", names):
                if _name in unique_farm_names:
                    continue
                unique_farm_names.append(_name)
        farm.farm_name = unique_farm_names

        resolution = resolve_postal_details_of_respondents(farm_data['attributes'])
        farm = create_respondents(farm, addressee_details, landowner_details, farmer_details)

        farm.warnings = farm_data['warnings']
        farm.warnings.update(get_postal_details_warnings(addressee_warning, farmer_warning, landowner_warning))

        farms_store[farm.catalogue_reference] = farm

        logger.info(f"Collating {index: 5d} for {farm.farm_reference}")

    return farms_store


def process_all_transcriptions(farms_store: dict[str, dict[str, Farm]]) -> list[tuple]:
    logger.info(" ===== PROCESSING TRANSCRIPTIONS for {county} ===== ")
    total_farms = len(farms_store)

    updated_farms = []
    for index, farm in enumerate(farms_store.values(), start=1):

        logger.info(f"Processsing: '{farm.catalogue_reference}'")
        transcriptions = [
            item
            for element in farm.source_data.values()
            for item in element
        ]
        processor = TranscriptionsProcessor(transcriptions)
        updated_farms.append((farm, processor.process_transcriptions()))

        logger.info(f"Processed {index: 5d} of {total_farms: 5d}: {farm.farm_reference}")

    return updated_farms


def write_farms_to_db(farms_store: dict[str, Farm], county: str, test_mode: bool = False) -> None:
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'c') as farm_db:
        farm_db[county] = farms_store.copy()


def read_farms_db(county: str, test_mode: bool = False) -> dict[str, Farm]:
    with shelve.open(PATH.TEST_DB if test_mode else PATH.FARMS_DB, 'r') as farm_db:
        farms_store = farm_db[county].copy()

    return farms_store


def create_farms(farms_store: dict[str, Farm], transcriptions: Iterator[Transcription]) -> dict[str, dict[str, Farm]]:
    for xscription in transcriptions:
        candidate_farm = Farm(xscription.county, xscription.parish, xscription.primary_farm_number)
        with dbm.open(PATH.FARM_IDS, 'c') as farm_ids_db:
            db_ids = farm_ids_db.get(candidate_farm.catalogue_reference, "")
            if db_ids:
                db_ids = eval(db_ids.decode())
                candidate_farm.id = db_ids['id']
                candidate_farm.replica_id = db_ids['replica_id']
            else:
                farm_ids_db[candidate_farm.catalogue_reference] = "{'id': '%s', 'replica_id': '%s'}" % (candidate_farm.id, create_uuid_str())
        form_type = xscription.document_type.name

        if candidate_farm.catalogue_reference not in farms_store:
            candidate_farm.source_data[form_type].append(xscription)
            farms_store[candidate_farm.catalogue_reference] = candidate_farm
            logger.info(f"NEW FARM: '{candidate_farm.catalogue_reference}' {candidate_farm.id} created from '{form_type}'")

        else:
            existing_farm = farms_store[candidate_farm.catalogue_reference]
            existing_farm.source_data[form_type].append(xscription)
            farms_store[candidate_farm.catalogue_reference] = existing_farm
            logger.info(f"{' '*50} '{candidate_farm.catalogue_reference}' {'.'*10} updated from '{form_type}'")

    return farms_store


def create_transcriptions(csv_data: Iterator[dict]) -> Generator[Transcription, None, None]:
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
            logger.info(f"Transcription created from row {row_number}")
            yield transcription

        except TranscriptionDataError as error_message:
            logger.error(f"Row {row_number} not processed because {error_message}")
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


def process_csv_files(test_mode: bool=False) -> None:
    input_files = PATH.TEST_INPUT.glob("*.csv") if test_mode else PATH.INPUT.glob("*.csv")

    for csv_file in input_files:
        county, _ = csv_file.stem.split("_", maxsplit=1)
        farms_store = {}   
        raw_farm_data: Iterator[dict] = load_data_from_file(csv_file)
        normalised_farm_data: Iterator[dict] = normalise_csv_data(raw_farm_data)
        transcriptions: Iterator[Transcription] = create_transcriptions(normalised_farm_data)
        farms_store: dict = create_farms(farms_store, transcriptions)
        write_farms_to_db(farms_store, county, test_mode)
        """ read from farm store - 
        this means that can comment out the loading and creation steps of the orchestration
        when only running Harvester to view changes to the proof output
        """
        farms_store = read_farms_db(county)
        farms_with_collated_attributes = process_all_transcriptions(farms_store)
        farms_store = update_farms(farms_store, farms_with_collated_attributes)
        write_farms_to_db(farms_store, county, test_mode)
        logger.info(" ===== CREATING PROOF FILES ===== ")
        create_proof_files(farms_store, county, csv_file.stem)


def main():
    logger.info(" ===== HARVESTING FARMS ===== ")
    process_csv_files()


if __name__ == "__main__":
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    process_csv_files()

