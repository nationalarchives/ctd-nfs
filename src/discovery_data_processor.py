"""
"""
from src._config.constants import PATH
from src._tools.xlreader import read_file


data_file = PATH.TEST_INPUT / "Rutland - Interim to Final.xlsx"


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
    discovery_data = []
    for row in raw_csv_data:
        cleaned_data_row = {}
        for key, value in row.items():
            if not value or type(value) is not str:
                cleaned_data_row[key] = value
                continue
            value = value.strip()
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


if __name__ == "__main__":
    excel_data = load_excel_data()
    cleaned_data = clean_excel_data(excel_data)

