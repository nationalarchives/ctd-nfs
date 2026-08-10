import os
import shelve
from pathlib import Path

import pytest

from src._dataclasses.farm_model import HarvestedFarm
from src._tools.constants import PATH
from src._tools.logging_setup import create_logger
from src.farm_harvester import create_proof_file, run_pipeline

logger = create_logger("src._config", "logging.yaml")


# @pytest.mark.skip(reason="awaiting refactoring of file_processor")
def test_file_processor():
    for file in Path(PATH.DB / "TEST").glob("*"):
        os.remove(file)

    run_pipeline(test_mode=True)

    with shelve.open(PATH.TEST_DB, 'r') as test_db:
        for reference in test_db.values():
            for farm in reference.values(): 
                assert isinstance(farm['farm'], Farm)
                # assert farm['source']


@pytest.mark.skip(reason="names and address distillation functions have been changed")
def test_proof_creation():
    create_proof_files(test_mode=True)



