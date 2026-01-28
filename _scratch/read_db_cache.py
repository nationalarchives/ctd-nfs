"""
Script to read and summarize contents of the api_cache.db file
created by create_api_cache.py
Must be run in the same directory where api_cache.db is located
"""
import shelve
from dataclasses import asdict
import pprint

from src._config.constants import PATH


pretty = pprint.PrettyPrinter(indent=4)

with shelve.open(PATH.TEST_DB, "r") as db:
    # db['RD Rutland'] = {}
    for county, catalogue_entry in db.items():
        for catalogue_reference, farm in catalogue_entry.items():
            print(f"{catalogue_reference}:")
            pretty.pprint(farm.field_info_date)
            # pretty.pprint(farm.source_data)

print("Done.")