import shelve
import os
from pathlib import Path

from src._config.constants import PATH
from src.harvester.file_processor import process_file
from src.harvester.farm_setup import Farm


def test_nfs_checks_and_mergers():
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    for csv_file in PATH.TEST_INPUT.glob("*.csv"):
        process_file(csv_file, test_mode=True)

    with shelve.open(PATH.TEST_DB, 'r') as test_db:
        for reference in test_db.values():
            for farm in reference.values(): 
                assert isinstance(farm['Farm'], Farm)
                assert farm['source']


