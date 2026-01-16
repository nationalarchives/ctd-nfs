from src._config.constants import PATH
from src.file_processor import process_file


if __name__ == "__main__":
    for csv_file in PATH.INPUT.glob("*.csv"):
        process_file(csv_file)

