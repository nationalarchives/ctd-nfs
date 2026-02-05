import shelve
import os
from pathlib import Path

from src._config.constants import PATH
from src.file_processor import process_file
from src.farm_builder import Farm

def test_nfs_checks_and_mergers():
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    for csv_file in PATH.TEST_INPUT.glob("*.csv"):
        process_file(csv_file, test_mode=True)

    with shelve.open(PATH.TEST_DB, 'r') as test_db:
        for county, reference in test_db.items():
            for catalogue_reference, farm in reference.items(): 
                assert isinstance(farm['Farm'], Farm)
                # print(f"\t{test_db[county][farm].field_info_date} -> {test_db[county][farm].primary_record_date}")

