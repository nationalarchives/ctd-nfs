from operator import itemgetter
import openpyxl
from openpyxl.styles import Alignment
from pathlib import Path
import string


class ExcelWriter:
    # TODO: create function to create Excel column letters for more than 26 columns
    column_letters = list(string.ascii_uppercase)
    column_letters.append('AA')

    def __init__(self):
        self._workbook = openpyxl.Workbook()

    def _write_row_data(self, _records):
        """

        :param _records:
        :return:
        """
        for row_idx, record in enumerate(_records, start=1):
            self._sheet.append(record)
            for col_idx in list(range(0, 25)):
                column = ExcelWriter.column_letters[col_idx]            
                self._sheet[f"{column}{row_idx + 1}"].alignment = Alignment(wrap_text=True, vertical='top')

    def _set_column_widths(self, _column_widths):
        for index, value in enumerate(_column_widths):
            column = ExcelWriter.column_letters[index]
            self._sheet.column_dimensions[column].width = value

    def _make_sheet(self, _index, sheet_name="", column_settings="", row_data=""):
        """
    
        :param _index:
        :param sheet_name:
        :param column_settings:
        :param row_data:
        :return:
        """
        self._workbook.create_sheet(index=_index, title=sheet_name)
        self._sheet = self._workbook[sheet_name]
        column_names = list(map(itemgetter(0), column_settings))
        column_widths = list(map(itemgetter(1), column_settings))
        self._set_column_widths(column_widths)
        self._sheet.append(column_names)
        self._write_row_data(row_data)

    def write_excel(self, _data: list, _file_name: Path):
        """

        :param _data:
        :param _file_name:
        :return:
        """
        for _index, sheet_data in enumerate(_data):
            self._make_sheet(_index, **sheet_data)
        del self._workbook['Sheet']
        self._workbook.save(_file_name)
