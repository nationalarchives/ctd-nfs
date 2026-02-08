"""
"""
from src._config.constants import PATH
from src._tools.xlreader import read_file


data_file = PATH.TEST_INPUT / "Rutland - Interim to Final.xlsx"


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

