"""
module for defining constants and constant namespaces.
"""

from pathlib import Path
import re
import calendar


class CSVandExcelNamespace():
    __slots__ = ()
    pass

class DataNamespace():
    __slots__ = ()

    CSV_HEADERS = [
        'filename_1',
        'filename_2',
        'document_type',
        'county',
        'parish',
        'primary_farm_number',
        'additional_farms',
        'farm_name',
        'addressee_title',
        'addressee_individual_name',
        'addressee_group_names',
        'address',
        'owner_title',
        'owner_individual_name',
        'owner_group_names',
        'owner_address',
        'farmer_title',
        'farmer_individual_name',
        'farmer_group_names',
        'farmer_address',
        'acreage',
        'OS_map_sheet',
        'field_info_date',
        'primary_record_date',
    ]
    DATE_FORMATS = [
        "%d %B %Y",
        "%d %B %y",
        "%d %b %Y",
        "%d %b %y",
        "%d %m %Y",
        "%d %m %y",
        "%B %Y",
        "%b %Y",
        "%Y",
    ]


class RegexNamespace():
    __slots__ = ()

    FORM_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    COVER_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)\.tif$""")
    
    _month_names: list = "|".join(list(calendar.month_name)[1:])
    _abbr_month_names: list = "|".join(list(calendar.month_abbr)[1:])
    _date_delimiters: str = r"""[\/\.\-\s]+"""

    DAYMONTHYEAR = re.compile(fr"""^(?P<day>\d\d?) +(?P<month>{_month_names}) +(?P<year>\d\d\d\d)$""")
    MONTHYEAR = re.compile(fr"""^(?P<month>{_month_names}) +(?P<year>\d\d\d\d)$""")
    YEARONLY = re.compile(r"""^(?P<year>\d\d\d\d)$""")
    DDMONYEAR = re.compile(fr"""^(?P<day>\d\d?){_date_delimiters}(?P<month>{_abbr_month_names}){_date_delimiters}(?P<year>(\d\d)?\d\d)$""")
    DDMMYYYY = re.compile(fr"""^(?P<day>\d\d?){_date_delimiters}(?P<month>\d\d?){_date_delimiters}(?P<year>(\d\d)?\d\d)$""")
    
    REMOVE_DELIMITERS = re.compile(fr"{_date_delimiters}+")
    SURVEY_YEARS = re.compile(r'^((19)?(41|42|43))$')


class PathNamespace():
    __slots__ = ()
    
    _PIPELINE_ROOT = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline")
  
    _PIECE_LOOKUP_DB = Path("MAF 32 Piece Lookup Table.db")
    EXCEL_LOOKUP_FILE = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\MAF 32 Piece Lookup Table 04-12-2025.xlsx")  
    PIECE_LOOKUP_TABLE = _PIPELINE_ROOT / "0-DB" / _PIECE_LOOKUP_DB

    _FARMS_CACHE = Path("MAF 32 Farms.db")
    _TEST_CACHE = Path("Test Farms.db")
    FARMS_DB = _PIPELINE_ROOT / "0-DB" / _FARMS_CACHE
    TEST_DB = _PIPELINE_ROOT / "0-DB" / "TEST" / _TEST_CACHE

    INPUT = _PIPELINE_ROOT / "1-INPUT"
    TEST_INPUT = _PIPELINE_ROOT / "1-INPUT" / "TEST"
    
    TRANSFORM = _PIPELINE_ROOT / "3-TRANSFORM"
    ARCHIVE = _PIPELINE_ROOT / "4-ARCHIVE"
    OUTPUT = _PIPELINE_ROOT / "5-OUTPUT"


PATH = PathNamespace()
REGEX = RegexNamespace()
DATA = DataNamespace()
CSVEXCEL = CSVandExcelNamespace()

