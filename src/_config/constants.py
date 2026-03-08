"""
module for defining constants and constant namespaces.
"""

from pathlib import Path
import re
import calendar


class CSVandExcelNamespace():
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
    PROOF_COLUMNS = [   
        ('Reference', 20),
        ('Reference Warnings', 40),
        ('Filenames', 45),
        ('Filename Warnings', 60),
        ('Record consists of', 15),
        ('Type Warnings', 40),
        ('Farm number', 15),
        ('Farm or holding', 20),
        ('Addressee name', 40),
        ('Addressee name warnings', 40),
        ('Addressee address', 60),
        ('Addressee(s)', 75),
        ('Farmer name', 40),
        ('Farmer name warnings', 40),
        ('Farmer address', 60),
        ('Farmer(s) or occupier(s)', 75),
        ('Landowner name', 40),
        ('Landowner name warnings', 40),
        ('Landowner address', 60),
        ('Landowner(s)', 75),
        # ('Acreage', 20),
        # ('Appears on Ordnance Survey sheet(s)', 20),
        # ('Field information date', 15),
        # ('Field Date Warnings', 20),
        # ('Primary farm record date', 15),
        # ('Primary Date Warnings', 20)
    ]


class DataNamespace():
    __slots__ = ()
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
        "%d %B",
        "%d %b",
        "%b",
        "%B",
    ]
    MONTH_NAMES: list = list(calendar.month_name)
    ABBR_MONTH_NAMES: list = list(calendar.month_abbr)
    DISCOVERY_API_URI = r"https://discovery.nationalarchives.gov.uk/API"
    DESCRIPTION_FIELDS = [
        'Farm Number',
        'Farm or holding',
        'Addressee(s)',
        'Farmer(s) or occupier(s)',
        'Landowner(s)',
        'Acreage',
        'Appears on Ordnance Survey sheet(s)',
        'Field information date',
        'Primary farm record date',
        'Record consists of',
    ]


class RegexNamespace():
    __slots__ = ()

    FORM_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    COVER_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)\.tif$""")   
    
    _date_delimiters: str = r"""[\/\.\-\s]+"""
    _month_names: list = "|".join(DataNamespace.MONTH_NAMES[1:])
    _abbr_month_names: list = "|".join(DataNamespace.ABBR_MONTH_NAMES[1:])

    DAYMONTHYEAR = re.compile(fr"""^(?P<day>\d\d?) +(?P<month>{_month_names}) +(?P<year>\d\d\d\d)$""")
    MONTHYEAR = re.compile(fr"""^(?P<month>{_month_names}) +(?P<year>\d\d\d\d)$""")
    YEARONLY = re.compile(r"""^(?P<year>\d\d\d\d)$""")
    DDMONYEAR = re.compile(fr"""^(?P<day>\d\d?){_date_delimiters}(?P<month>{_abbr_month_names}){_date_delimiters}(?P<year>(\d\d)?\d\d)$""")
    DDMMYYYY = re.compile(fr"""^(?P<day>\d\d?){_date_delimiters}(?P<month>\d\d?){_date_delimiters}(?P<year>(\d\d)?\d\d)$""")
    DAYMONTH = re.compile(fr"""^(?P<day>\d\d?) +(?P<month>{_month_names})$""")
    DAYMON = re.compile(fr"""^(?P<day>\d\d?) +(?P<month>{_abbr_month_names})$""")
    MONTH = re.compile(fr"""^(?P<month>{_month_names}|)$""")
    MON = re.compile(fr"""^(?P<month>{_abbr_month_names})$""")
    
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
    DB = _PIPELINE_ROOT / "0-DB"
    FARMS_DB = DB / _FARMS_CACHE
    TEST_DB = DB / "TEST" / _TEST_CACHE

    INPUT = _PIPELINE_ROOT / "1-INPUT"
    TEST_INPUT = INPUT / "TEST"
    
    TRANSFORM = _PIPELINE_ROOT / "3-TRANSFORM"
    ARCHIVE = _PIPELINE_ROOT / "4-ARCHIVE"
    OUTPUT = _PIPELINE_ROOT / "5-OUTPUT"
    TEST_OUTPUT = OUTPUT / "TEST"


PATH = PathNamespace()
REGEX = RegexNamespace()
DATA = DataNamespace()
CSVEXCEL = CSVandExcelNamespace()

