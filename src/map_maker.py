"""map_maker.py

This module will extract map sheet data provided in an Excel and store it in the disk cache, for later use by the publisher module
"""
import shelve

from src._tools.constants import DB, PATH, REGEX
from src._tools.helpers import (
    clean_excel_data,
    create_uuid_str,
    load_excel_data,
    read_county_data_from_cache,
)
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


def confirm_maps_written_to_cache(county_code: str) -> None:
    with shelve.open(DB.PRODUCTION, 'r') as diskcache:
        county_data = diskcache[county_code].copy()

    for maps in county_data['MAF73'].values():
        for _map_ref in maps:
            logger.info(f"Map sheet data for {_map_ref} added to cache")


def write_maps_to_cache(map_data: list[dict], county_code: str, version: str, test_mode: bool = False) -> None:
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

    with shelve.open(DB.TEST if test_mode else DB.PRODUCTION, 'c') as farm_db:
        county_store = farm_db[county_code].copy()
        county_store['MAF73'].update({version: maps_cache})
        farm_db[county_code] = county_store.copy()


def add_ids_to_maps(map_data: list[dict], existing_maps: dict) -> list[dict]:
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


def main() -> None:
    """_summary_

    Keyword Arguments:
        test_mode -- _description_ (default: {False})
    """    
    input_files = PATH.INPUT.glob("*MAF73*.xlsx")
    for map_file in input_files:
        if map_file.name.startswith("Index"):
            continue
        county_code, _ = map_file.name.split(" ", maxsplit=1)
        file_version = REGEX.FILE_VERSION.match(map_file.stem)['version']
        build_version, _ = file_version.split("-")

        proof_data = load_excel_data(map_file)
        map_data = clean_excel_data(proof_data)

        county_from_db = read_county_data_from_cache(county_code, 'MAF73')
        existing_maps = county_from_db.get('build_version', {})
        map_data_with_ids = add_ids_to_maps(map_data, existing_maps)          

        write_maps_to_cache(map_data_with_ids, county_code, build_version)
        confirm_maps_written_to_cache(county_code)


if __name__ == "__main__":
    main()

