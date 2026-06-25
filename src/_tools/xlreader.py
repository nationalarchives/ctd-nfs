"""
xlreader.py
Extracts data from xls and xlsx files
Data is extracted as a dictionary where key: value refers to sheet_name: [rows of data as a list of tuples]
"""
from typing import Union
import io
import logging

from xlrd import open_workbook
from xlrd.biffh import XLRDError
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException


logger = logging.getLogger(__name__)


def read_excel_2007(xls_file: Union[str, bytes]) -> dict[list[tuple]]:
    """
    uses xlrd module to read data from 2003/2007 Excel (i.e. ending in .xls)
    :param xls_file:
    :return:
    """
    workbook = open_workbook(xls_file, encoding_override='utf_8', formatting_info=False)
    return {
        sheet.name: [
            sheet.row_values(row, 0, sheet.ncols)
            for row in range(sheet.nrows)
            ]
        for sheet in workbook.sheets()
        }


def read_excel_2010(xlsx_file: Union[str, bytes]) -> dict[list[tuple]]:
    """
    uses openpyxl module to read data from 2010 Excel (i.e. ending in .xlsx)
    :param xlsx_file:
    :return:
    """
    workbook = load_workbook(filename=xlsx_file, read_only=True, data_only=True)
    return {
        sheet.title: list(sheet.iter_rows(max_row=sheet.max_row, values_only=True))
        for sheet in workbook.worksheets
    }


# @log_decorator()
def read_file(excel_file: Union[str, bytes]) -> dict[list[tuple]]:
    """
    
    :param excel_file:
    :return:
    """
    
    with open(excel_file, "rb") as file_pointer:
        in_mem_file = io.BytesIO(file_pointer.read())
    
    try:
        return read_excel_2010(in_mem_file)
    except InvalidFileException:
        return read_excel_2007(in_mem_file)
    except XLRDError:
        logger.error("Unsupported format, or corrupt file: please make sure file is valid xls or xlsx file with correct extension")


if __name__ == "__main__":
    import pprint
    
    pptr = pprint.PrettyPrinter(indent=4)
    files = [
        r"C:\Users\rbruno\OneDrive - The National Archives\Projects\EHRI\Data\TNA collections WO 311 German concentration camp staff_ready.xlsx",
        ]
    for file in files:
        pptr.pprint(read_file(file))
