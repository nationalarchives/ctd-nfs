import dbm
import json
import re
import shelve
from collections.abc import Iterable
from pathlib import Path

from src._tools.constants import DB, PATH, REGEX

with dbm.open(DB.DB.joinpath("Farm_IDs.db"), 'c') as farm_db, dbm.open(DB.DB.joinpath("File_IDs.db"), 'c') as files_db:
    for json_data in load_jsons():
        # farm_db[json_data['record']['citableReference']] = f"""{'id': {json_data['record']['iaid']}, 'replica_id': {json_data['record']['replicaId']}}"""
        farm_db[json_data['record']['citableReference']] = "{'id': '%s', 'replica_id': '%s'}" % (json_data['record']['iaid'], json_data['record']['replicaId'])
        print(f"{farm_db[json_data['record']['citableReference']].decode()}")
        for item in json_data['replica']['files']:
            files_db[item['originalName']] = f"{REGEX.IMAGE_ID.match(item['name'])['id']}"
            print(f"{files_db[item['originalName']].decode()}")


with dbm.open(DB.DB.joinpath("Farm_IDs.db"), 'r') as farm_db:
    print(f"{farm_db['MAF 32/346/5/14']=}")
    for reference, ids_string in farm_db.items():
        ids = eval(ids_string.decode())
        print(f"{reference=}, {ids['id']=}")

with dbm.open(DB.DB.joinpath("File_IDs.db"), 'r') as files_db:
    print(f"{files_db['MAF32-348-56_69.tif']=}")
    for file_name, id in files_db.items():
        print(f"{file_name=}, {id=}")


def create_map_objects_with_ids_from_jsons(json_data: Iterable[dict]) -> dict:
    return {
        json_doc['record']['citableReference']: {'id': json_doc['record']['iaid'], 'replica_id': json_doc['record']['replicaId']}
        for json_doc in json_data
    }


def load_jsons(json_files: Iterable[Path]) -> Iterable[dict]:
    for _file in json_files:
        with open(_file) as file_obj:
            yield json.load(file_obj)


def get_maf73_jsons(county_code: str) -> Iterable[Path]:
    return PATH.PUBLISH.glob(f"{county_code}/MAF73/V1/*.json")


counties = [
    "BD",
    "BK",
    "CB",
    "HD",
    "HN",
    "IE",
    "IW",
    "KT",
    "MX",
    "OX",
    "RD",
    "SK",
    "SW",
    "XW",
    "YN",
]


def main():
    for county_code in counties:
        json_files = get_maf73_jsons(county_code)
        json_data = load_jsons(json_files)
        map_objects = create_map_objects_with_ids_from_jsons(json_data)

        with shelve.open(DB.PRODUCTION, 'c') as disk_cache:
            county_cache = disk_cache[county_code].copy()


if __name__ == "__main__":
    main()


