"""Add unique ids for each row of V1 transcription csv file

V1 files created by the CTD team have an empty ID column. 
This script creates a unique ID value for each row and creates a new file with the ID column populated with values
The file name is edited - the edit version at the end of the file name ('00') is incremented to '01'
e.g., 
"AY Anglesey_MAF32_HarvesterIN_V1-20261104-00.csv" becomes "AY Anglesey_MAF32_HarvesterIN_V1-20261104-01.csv"

NOTE: Ensure that the original file does not have empty columns after the ID column - these must be removed before running the script (in Notepad++)
"""
import csv
from collections.abc import Generator, Iterator
from pathlib import Path

from src._tools.constants import CSVEXCEL, PATH


def load_data_from_file(csv_file: Path) -> Generator[dict]:
    with open(csv_file, newline='') as file_obj:
        raw_csv_data = csv.DictReader(file_obj, skipinitialspace=True)
        yield from raw_csv_data


def main():
    csv_00_files = PATH.INPUT.glob("*MAF32_HarvesterIN_V*-*-00.csv")
    for csv_file in csv_00_files:
        county_code, _ = csv_file.stem.split(" ", maxsplit=1)
        transcription_rows: Iterator[dict] = load_data_from_file(csv_file)
        updated_rows = []
        for counter, row_in in enumerate(transcription_rows, start=1):
            row_in['ID'] = f"{county_code}{counter:06d}"
            updated_rows.append(row_in)

        csv_01_file = PATH.INPUT / Path(str(csv_file.name).replace("-00", "-01"))
        with open(csv_01_file, 'w', newline='') as out_csv:
            writer = csv.DictWriter(out_csv, fieldnames=CSVEXCEL.CSV_HEADERS)
            writer.writeheader()
            writer.writerows(updated_rows)


if __name__ == "__main__":
    main()