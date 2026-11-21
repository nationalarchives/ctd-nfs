"""Module to report whether all the farm documents built for each county have been successfully ingested & indexed in Discovery

Two sets will be created and compared:
- the ids of the locally stored JSON documents built for each county
- the ids of each farm record found on Discovery by querying the database via the Discovery API

The Discovery ids of the county's parishes will be used as a search term to the API
This query return the records of all the farms in the parish

The set of parish ids will retrieved from the farm documents
"""
import json
from collections.abc import Iterable

from src._tools.constants import PATH


def get_indexed_record_ids():
    """Retrieve ids of farm records for specific county indexed in Discovery
    """
    
    """
    get all parish references for county from piece lookup table
    
    for each parish reference
        retrieve records of all farms in parish via Discovery API
    
    """


def get_farm_and_parish_ids(farm_documents: Iterable[dict]) -> dict:
    """Generate a list of farm iaids and a set of parish ids from the farm documents

    The parish ids will be used as the query to the Discovery API - 
    creating this set means that it is not necessary to make a separate call to the API to find out the 

    Arguments:
        farm_documents -- _description_

    Returns:
        _description_
    """    
    iaids: list[str] = []
    parish_ids: dict[str, str] = {}

    for _document in farm_documents:
        iaids.append(_document['record']['iaid'])
        suffix = f"/{_document['record']['referencePart']}"
        parish_reference = _document['record']['citableReference'].removesuffix(suffix)
        if parish_reference not in parish_ids:
            parish_ids[parish_reference] = _document['record']['parentId']

    return {
        'iaids': iter(iaids),
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
    print(f"{ids['parish_ids']=}, {next(ids['iaids'])=}")

    # ids_of_indexed_farms = get_series_from_api(parish_references[0])
    # print(f"{ids_of_indexed_farms}")
    


if __name__ == "__main__":
    main()
