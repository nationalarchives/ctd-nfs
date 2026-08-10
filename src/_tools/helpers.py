import logging
import re
import uuid
from pathlib import Path

from src._tools.xlreader import read_file

logger = logging.getLogger(__name__)

def create_uuid_str():
    return f"{uuid.uuid4()}"


class TranscriptionDataError(Exception):
    """A base class for all business rule validation exceptions"""


class ValueObject:
    """A base class for all value objects"""


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value) if item != "*"]


def load_excel_data(data_file: Path) -> list[dict]:
    logger.info(F" ===== LOADING PROOF FILE {data_file.name}===== ")
    excel_data = read_file(data_file)

    column_names = excel_data['Proof data'][0]

    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data["Proof data"][1:]
        if row_data[0]
    ]


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
    logger.info(" ===== CLEANING PROOF DATA ===== ")
    discovery_data = []
    non_breaking_space = "\xa0"
    for row in raw_csv_data:
        cleaned_data_row = {}
        for key, value in row.items():
            if not value or type(value) is not str:
                cleaned_data_row[key] = value
                continue

            value = value.strip()
            value = value.replace(f"{non_breaking_space}", " ")
            value = value.replace("\n", "")
            value = re.sub(r";\s*", "; ", value)
            cleaned_data_row[key] = value

        discovery_data.append(cleaned_data_row)

    return discovery_data

