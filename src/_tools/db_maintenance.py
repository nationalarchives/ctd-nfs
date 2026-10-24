import dbm
import json
import re
from collections.abc import Iterable

from src._tools.constants import DB, REGEX


def load_jsons() -> Iterable[dict]:
    for input_json in DB.PUBLISH.joinpath("RD Rutland").glob("*.json"):
        with open(input_json) as json_file:
            yield json.load(json_file)


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


def main():
    pass


if __name__ == "__main__":
    main()


