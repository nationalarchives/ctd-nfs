"""Module to report whether all the farm documents built for each county have been successfully ingested & indexed in Discovery

Two sets will be created and compared:
- the ids of the locally stored JSON documents built for each county
- the ids of each farm record found on Discovery by querying the database via the Discovery API

The Discovery ids of the county's parishes will be used as a search term to the API
This query return the records of all the farms in the parish

The set of parish ids will retrieved from the farm documents
"""
import json
import pprint
import time
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor
from itertools import batched
from pathlib import Path
from time import sleep

import requests

from src._tools.constants import DISCOVERY, PATH

pretty = pprint.PrettyPrinter(indent=4)


def get_ids_of_indexed_records(parish_ids: dict) -> set[str]:
    """Retrieve ids of farm records for specific county indexed in Discovery
    """   

    record_ids: set[str] = set()
    for batch_no, batch in enumerate(batched(parish_ids.items(), 100), start=1):
        for index, (parish_ref, parisb_id) in enumerate(batch, start=1):
            print(f"{batch_no:02d}{index:03d}: {parish_ref} ({parisb_id})", end=": ")
            api_query = f"{DISCOVERY.API_URI}/records/v1/children/{parisb_id}?limit=500"   
            result = requests.get(api_query)
            if result.status_code != 200:
                print(f"!!! API response {result.status_code}")
                continue

            data = result.json()
            print(f"{len(data['assets'])} records")          
            for item in data['assets']:
                record_ids.add(item['id'])

        print(f"==== {DISCOVERY.SPEED_BUMP_IN_SECONDS} SECOND SPEED BUMP ====")
        sleep(DISCOVERY.SPEED_BUMP_IN_SECONDS)
        
    print(f"-- TOTAL {len(record_ids)} records retrieved.")
    return record_ids


def get_farm_and_parish_ids(farm_documents: Iterable[dict]) -> dict:
    """Generate a list of farm iaids and a set of parish ids from the farm documents

    The parish ids will be used as the query to the Discovery API - 
    creating this set means that it is not necessary to make a separate call to the API to find out the 

    Arguments:
        farm_documents -- _description_

    Returns:
        _description_
    """    
    iaids: set[str] = set()
    parish_ids: dict[str, str] = {}

    for _document in farm_documents:
        iaids.add(_document['record']['iaid'])
        suffix = f"/{_document['record']['referencePart']}"
        parish_reference = _document['record']['citableReference'].removesuffix(suffix)
        if parish_reference not in parish_ids:
            parish_ids[parish_reference] = _document['record']['parentId']

    print(f"TOTAL {len(iaids)} farm & map documents built")
    return {
        'iaids': iaids,
        'parish_ids': parish_ids,
    }


def get_document(_file: Path) -> dict:
    with open(_file) as file_obj:
        print(f"\t... {_file.stem}")
        return json.load(file_obj)


def get_farm_documents(county_code: str) -> Iterable[dict]:
    """Return farm documents as a generator
    """
    print(f"COUNTY: {county_code}\nProcessing documents:")
    document_paths = PATH.PUBLISH.glob(f"{county_code}/MAF*/V1/*.json")
    with ProcessPoolExecutor() as executor:
        return executor.map(get_document, document_paths)


def main():
    """
    Retrieve ids of farm records for specific county indexed in Discovery
    Retrieve ids of farm documents stored locally
    Compare sets of ids
    Report result
    """
    county_code = "YW"

    start_time = time.perf_counter()    
    farm_documents = get_farm_documents(county_code)
    load = time.perf_counter() - start_time
    print(f"get_farm_documents took {load} seconds")

    ids_from_documents = get_farm_and_parish_ids(farm_documents)

    ids_of_indexed_farms = get_ids_of_indexed_records(ids_from_documents['parish_ids'])

    difference = ids_from_documents['iaids'] - ids_of_indexed_farms
    print(difference) if difference else print("ALL INDEXED")


if __name__ == "__main__":
    main()
