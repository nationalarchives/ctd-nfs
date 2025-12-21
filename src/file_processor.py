from pathlib import Path
from typing import Generator
import csv


def load_data_from_file(csv_file: Path) -> Generator[dict, None, None]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        Generator[dict, None, None]: _description_
    """

    try:
        print(f"Processing file: {csv_file.stem}")
        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
        return iter(raw_csv_data)
    
    except csv.Error as csv_error_message:
        print(f"!!! ERROR in data loading: {csv_error_message}")

