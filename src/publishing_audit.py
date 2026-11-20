"""Module to report whether all the farm documents built for each county have been successfully ingested & indexed in Discovery

Two sets will be created and compared:
- the ids of the locally stored JSON documents built for each county
- the ids of each farm record found on Discovery by querying the database via the Discovery API

The parish reference as a search term to the API e.g., 'MAF 32/1/40"
This query return the records of all the farms in the parish

The list of all the parish references in a county will be retrieved from the piece lookup table
"""
import json
from collections.abc import Iterable
from pathlib import Path

from src._tools.constants import DB, PATH


def get_parish_references_in_county(county_code: str) -> list[str]:
    """Retrieve parish references from piece lookup table
    """
    return [
        row['Catalogue ref']
        for row in DB.PIECES
        if row['County Code'] == county_code
    ]


def get_indexed_record_ids():
    """Retrieve ids of farm records for specific county indexed in Discovery
    """
    
    """
    get all parish references for county from piece lookup table
    
    for each parish reference
        retrieve records of all farms in parish via Discovery API
    
    """


def get_ids_of_farm_documents(county_code: str) -> Iterable[str]:
    """Retrieve ids of farm documents for specific county which were sent to Discovery
    """    
    for _file in PATH.PUBLISH.glob(f"{county_code}/MAF32/V1/*.json"):
        with open(_file) as file_obj:
            document = json.load(file_obj)
            yield document['record']['iaid']


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

    parish_references = get_parish_references_in_county("SK")
    print(f"{parish_references}")
    


if __name__ == "__main__":
    main()
