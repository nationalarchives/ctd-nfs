import shelve
import os

from src._config.constants import PATH
from src.file_processor import process_file


def test_nfs_checks_and_mergers():
    for csv_file in PATH.TEST_INPUT.glob("*.csv"):
        process_file(csv_file, test_mode=True)

    with shelve.open(PATH.TEST_DB, 'r') as test_db:
        for county, farms in test_db.items():
            assert len(farms) > 1

    os.remove(PATH.TEST_DB)