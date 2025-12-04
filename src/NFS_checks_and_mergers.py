from pathlib import Path
import csv
from typing import Generator

from farm_class_setup import clean_csv_data, Farm
from pre_instantiation_checks import perform_pre_instantiation_checks


CSV_FILES = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Samples")


def load_data_from_file(csv_file: Path) -> list[dict]:
    """_summary_

    Args:
        csv_file (Path):  

    Returns:
        dict: _description_
    """
    
    try:
        print(f"Processing file: {csv_file.stem}")

        with open(csv_file, newline='') as file_obj:
            raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True) 
            cleaned_data: list[dict] = clean_csv_data(raw_csv_data)
    except csv.Error as csv_error_message:
        print(f"!!! ERROR in data loading: {csv_error_message}")

    return cleaned_data


def convert_to_generator(csv_data: list[dict]) -> Generator[dict, None, None]:
    """_summary_

    Args:
        csv_data (list[dict]): _description_

    Yields:
        dict: _description_
    """
    for index, row in enumerate(csv_data):
        row['row_number'] = index
        yield row

if __name__ == "__main__":
    csv_files = CSV_FILES.glob("*.csv")

    for csv_file in csv_files:
        if csv_file.name != "Rutland Edited Data for RALPH.csv":
            continue
        try:
            cleaned_farm_data: list[dict] = load_data_from_file(csv_file)
            farm_data_generator = convert_to_generator(cleaned_farm_data)
            for farm_data_row in farm_data_generator:
                print(f"\nProcessing row {farm_data_row['row_number']} of file {csv_file.stem}")
                reference_values, warnings = perform_pre_instantiation_checks(farm_data_row)
                farm = Farm(farm_data_row)
                print(f"Successfully instantiated Farm: {farm.county=}")

        except ValueError as value_error_msg:
            print(f"Failed to instantiate Farm from data: {value_error_msg}")