"""
"""
from urllib import parse
import requests

from src._config.constants import PATH, DATA
from src._tools.xlreader import read_file
from src.record_builder import Record


data_file = PATH.TEST_INPUT / "Rutland - Interim to Final.xlsx"


def get_parent_id(raw_reference: str) -> str:
    ref = raw_reference.rsplit("/", maxsplit=1)[0]
    ref_url_safe = parse.quote(ref)

    api_query = fr"{DATA.DISCOVERY_API_URI}/search/records?sps.searchQuery={ref_url_safe}"
    result = requests.get(api_query)

    parent_record = result.json()
    return parent_record['records'][0]['id']


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
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
            cleaned_data_row[key] = value
        discovery_data.append(cleaned_data_row)
    
    return discovery_data


def load_excel_data() -> list[dict]:
    excel_data = read_file(data_file)
    column_names = excel_data['Sheet'][0]
    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data["Sheet"][1:]
        if row_data[0]
    ]


def create_description(row_data: dict) -> str:
    scope_and_content = [
    f"{key}: {row_data[key]}<p>"
    for key in DATA.DESCRIPTION_FIELDS
    ]
    return "".join(scope_and_content)


if __name__ == "__main__":
    excel_data = load_excel_data()
    cleaned_data = clean_excel_data(excel_data)

    for row in cleaned_data:
        parent_id = get_parent_id(row['Reference'])
        description = create_description(row)

        record = Record(
            citableReference=row['Reference'],
            parentId=parent_id,
            scopeContent={'description': description},
            title=row['Farm Number'],
        )

