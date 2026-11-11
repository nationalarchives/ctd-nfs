import json
import pprint
import shelve
from collections.abc import Iterable
from pathlib import Path
from random import choice

from src._tools.constants import DB, PATH
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")
pretty = pprint.PrettyPrinter(indent=4)


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
	# "AY",
	# "BM",
	# "DY",
	# "HP",
	# "LH",
	# "LK",
	# "LL",
	# "LR",
	# "NK",
	# "NM",
	# "NN",
	# "SE",
	# "SY",
	# "XE",
	# "YE",
	# "YW",
	"IW",
	"RD",
]


def main():
    with shelve.open(DB.PRODUCTION, 'c') as disk_cache:
        for county_code in counties:
            logger.info(f"Retrieving MAF73 data for {county_code}")
            json_files = get_maf73_jsons(county_code)
            json_data = load_jsons(json_files)
            map_objects = create_map_objects_with_ids_from_jsons(json_data)

            logger.info("--- Caching MAF3 data")
            county_cache = disk_cache[county_code].copy()
            county_cache.update({'MAF73': {'V1': map_objects}})
            disk_cache[county_code] = county_cache.copy()

    with shelve.open(DB.PRODUCTION, 'r') as disk_cache:
        while True:
            county_code = choice(counties)
            if county_code != 'AY':
                break
        print(f"{county_code=}")
        county_cache = disk_cache[county_code].copy()
        pretty.pprint(object=choice(list(county_cache['MAF73']['V1'].values())))
        pretty.pprint(choice(list(county_cache['V1'].values())))

if __name__ == "__main__":
    main()


