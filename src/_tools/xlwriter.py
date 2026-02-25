from operator import itemgetter
import openpyxl
from pathlib import Path
import string


class ExcelWriter:
    column_letters = string.ascii_uppercase

    def __init__(self):
        self._workbook = openpyxl.Workbook()

    def _write_row_data(self, _records):
        """

        :param _records:
        :return:
        """
        for record in _records:
            self._sheet.append(record)

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
