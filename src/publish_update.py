import shelve
import tomllib
from pathlib import Path

from src._tools.constants import DB, PATH, REGEX
from src._tools.helpers import clean_excel_data, create_uuid_str, load_excel_data
from src._tools.logging_setup import create_logger
from src.farm_harvester import read_farms_db
from src.map_publisher import (
    build_catalogue_documents,
    write_catalogue_documents,
    write_jsons_to_zip_archive,
)

logger = create_logger("src._config", "logging.yaml")


def write_maps_to_db(map_data: list[dict], county_code: str, version: str, test_mode: bool = False) -> None:
    """_summary_

    Arguments:
        maps_store -- _description_
        county -- _description_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})
    """    
    maps_cache = {
        map_proof['Reference']: map_proof
        for map_proof in map_data
    }

    with shelve.open(DB.PRODUCTION, 'c') as farm_db:
        county_store = farm_db[county_code].copy()
        county_store['MAF73'].update({version: maps_cache})
        farm_db[county_code] = county_store.copy()


def get_existing_map_ids(map_data: list[dict], existing_maps: dict) -> list[dict]:
    amended_map_data: list[dict] = []

    for map in map_data:
        if map['Reference'] in existing_maps:
            map['id'] = existing_maps[map['Reference']]['id']
            map['replica_id'] = existing_maps[map['Reference']]['replica_id']
        else:
            map['id'] = create_uuid_str()
            map['replica_id'] = create_uuid_str()

        amended_map_data.append(map)

    return amended_map_data


def process_proof_files(config: dict) -> None:
    xlsx_files = PATH.INPUT.glob("TEST/*MAF73*.xlsx") if config['test_mode'] else PATH.INPUT.glob("*MAF73*.xlsx")

    for proof_file in xlsx_files:
        county_code, _ = proof_file.name.split(" ", maxsplit=1)
        if (version := REGEX.TRANSCRIPTIONS_VERSION.match(proof_file.stem)['version']) in ["V0", "V1"]:
            logger.error("Input file version must be V2 or above")
            continue

        proof_data = load_excel_data(proof_file)
        map_data = clean_excel_data(proof_data)

        county_from_db = read_farms_db(county_code, config['test_mode'])
        existing_maps = {}
        for version_number in county_from_db['MAF73']:
            existing_maps.update(county_from_db['MAF73'][version_number])

        map_data_with_exising_ids = get_existing_map_ids(map_data, existing_maps)          
        final_documents = build_catalogue_documents(map_data_with_exising_ids, config['update_scope'])
        write_catalogue_documents(final_documents, county_code, version)
        write_jsons_to_zip_archive(county_code, version)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    with open(Path(r"src/run_options.toml"), mode="rb") as fp:
        config = tomllib.load(fp)

    process_proof_files(config['map_publisher'])


if __name__ == "__main__":
    main(test_mode=False)

