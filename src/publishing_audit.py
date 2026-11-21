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
from collections.abc import Iterable
from time import sleep

import requests

from src._tools.constants import DISCOVERY, PATH

pretty = pprint.PrettyPrinter(indent=4)


def get_ids_of_indexed_records(parish_ids: dict) -> set[str]:
    """Retrieve ids of farm records for specific county indexed in Discovery
    """   

    record_ids: set[str] = set()
    for par_ref, par_id in parish_ids.items():
        print(f"{par_ref} ({par_id})", end=": ")
        api_query = f"{DISCOVERY.API_URI}/records/v1/children/{par_id}?limit=500"   
        result = requests.get(api_query)
        if result.status_code != 200:
            print(f"!!! API response {result.status_code}")
            continue

        data = result.json()
        print(f"{len(data['assets'])} records")          
        for item in data['assets']:
            record_ids.add(item['id'])

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

    return {
        'iaids': iaids,
        'parish_ids': parish_ids,
    }


def get_farm_documents(county_code: str) -> Iterable[dict]:
    """Return farm documents as a generator
    """    
    for _file in PATH.PUBLISH.glob(f"{county_code}/MAF32/V1/*.json"):
        with open(_file) as file_obj:
            yield json.load(file_obj)


def main():
    """
    Retrieve ids of farm records for specific county indexed in Discovery
    Retrieve ids of farm documents stored locally
    Compare sets of ids
    Report result
    """
    # for index, id in enumerate(get_ids_of_farm_documents("SK")):
    #     print(f"{id=}")
    # print(f"Total documents {index}")

    farm_documents = get_farm_documents("SK")
    ids = get_farm_and_parish_ids(farm_documents)

    ids_of_indexed_farms = get_ids_of_indexed_records(ids['parish_ids'])
    # print(f"{ids_of_indexed_farms}")
    


if __name__ == "__main__":
    main()
