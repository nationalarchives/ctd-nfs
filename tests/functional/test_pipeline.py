import shelve
import os
from pathlib import Path

from src._config.constants import PATH
from src.harvester.file_processor import process_csv_files
from src.harvester.catalogue_proofs_builder import create_proof_files
from src.harvester.farm_setup import Farm
from src._tools.logging_setup import create_logger


logger = create_logger("src._config", "logging.yaml")


def test_file_processor():
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    process_csv_files(test_mode=True)

    with shelve.open(PATH.TEST_DB, 'r') as test_db:
        for reference in test_db.values():
            for farm in reference.values(): 
                assert isinstance(farm['Farm'], Farm)
                assert farm['source']


def test_proof_creation():
    create_proof_files(test_mode=True)



