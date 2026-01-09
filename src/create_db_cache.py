"""
    Creates a shelve database from an excel lookup table

Returns:
    _type_: _description_
"""
from pathlib import Path
import shelve

from src._tools.xlreader import read_file

from src._config.constants import DATA, EXCEL_LOOKUP_FILE


def read_records_from_file(excel_file: Path) -> list[dict]:  
    """
    Reads data from file as a dictionary where each {key, value} refers to one sheet and its rows (a list of tuples) 
    Returns a list of dictionaries, using the first row as the header

    Args:
        excel_file (Path):

    Returns:
        list[dict]: 
    """
    file_data = read_file(excel_file)
    sheet_name = list(file_data.keys())[0]
    data_rows = file_data[sheet_name]
    return [
        dict(zip(data_rows[0], row))
        for row in data_rows[1:]
        if row[1]
    ]


if __name__ == "__main__":

    lookup_table: list[dict] = read_records_from_file(EXCEL_LOOKUP_FILE)
    with shelve.open(DATA.PIECE_LOOKUP_TABLE) as shelf:
        shelf['pieces lookup table'] = lookup_table
        pass

