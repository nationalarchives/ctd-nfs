import shelve

from src._config.constants import DATA, REGEX
from src.file_processor import process_file


if __name__ == "__main__":
    with shelve.open(DATA.PIECE_LOOKUP_TABLE, "r") as piece_lookup_db:   
        county_names = piece_lookup_db['County names']

    for csv_file in DATA.INPUT.glob("*.csv"):
        if REGEX.COUNTY_NAME.match(csv_file.name)["county_name"] in county_names:
            process_file(csv_file)
        # print(f"{Farm.all_farms=}")