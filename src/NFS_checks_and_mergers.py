from src._config.constants import DATA
from src.file_processor import process_file


if __name__ == "__main__":
    for csv_file in DATA.INPUT.glob("*.csv"):
        process_file(csv_file)
        # print(f"{Farm.all_farms=}")