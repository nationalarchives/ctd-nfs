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
        'notes',
    ]
    PROOF_COLUMNS = [   
        ('catalogue_reference', 20),
        ('Reference Warnings', 40),
        ('farm_id', 50),
        ('replica_id', 60),
        ('file_ids', 60),
        ('file_names', 60),
        ('Filename Warnings', 40),
        ('forms', 15),
        ('Type Warnings', 40),
        ('farm_number', 15),
        ('farm_name', 20),
        ('addressee_name', 40),
        ('Addressee name warnings', 40),
        ('addressee_address', 60),
        ('addressee', 75),
        ('farmer_name', 40),
        ('Farmer name warnings', 40),
        ('farmer_address', 60),
        ('farmer', 75),
        ('landowner_name', 40),
        ('Landowner name warnings', 40),
        ('landowner_address', 60),
        ('landowner', 75),
        ('acreage', 30),
        ('os_sheet_number', 30),
        ('field_info_date', 25),
        ('primary_record_date', 25),
    ]


class DataNamespace():
    __slots__ = ()
    FORM_TYPES = [
		'C 47/SSY',
		'C 49/SSY',
		'C51/SSY',
		'SF',
		'SF C69/SSY',
		'B496/EI',
		'Other',
		'Cover',
    ]   
    FARM_DATA_FIELDS = [
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
        "%d %B",
        "%d %b",
        "%b",
        "%B",
    ]
    MONTH_NAMES: list = list(calendar.month_name)
    ABBR_MONTH_NAMES: list = list(calendar.month_abbr)


class RegexNamespace():
    __slots__ = ()

    FORM_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)(?:-\d)?_+(?P<image_number>\d+)\.tif$""")
    COVER_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)(?:-\d)?\.tif$""")   
    
    _date_delimiters: str = r"""[\/\.\-\s]+"""
    _month_names: str = "|".join(DataNamespace.MONTH_NAMES[1:])
    _abbr_month_names: str = "|".join(DataNamespace.ABBR_MONTH_NAMES[1:])

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
    IMAGE_ID = re.compile(r"""^66\/MAF\/32\/(?P<id>.*?)\.jpg$""")


class PathNamespace():
    __slots__ = ()
    
    _PIPELINE_ROOT = Path(r"Pipeline")
  

    _FARMS_CACHE = Path("MAF 32 Farms.db")
    _TEST_CACHE = Path("Test Farms.db")
    
    DB = _PIPELINE_ROOT / "#ADMIN" / "DB"
    EXCEL_LOOKUP_FILE = DB / "MAF 32 Piece Lookup Table 04-12-2025.xlsx"
    PIECE_LOOKUP_TABLE = DB / "MAF 32 Piece Lookup Table.db"
    
    FARMS_DB = DB / _FARMS_CACHE
    TEST_DB = DB / "TEST" / _TEST_CACHE

    INPUT = _PIPELINE_ROOT / "1-INPUT"
    TEST_INPUT = INPUT / "TEST"
    
    HARVEST = _PIPELINE_ROOT / "2-HARVEST"
    TEST_OUTPUT = HARVEST / "TEST"
    
    PUBLISH = _PIPELINE_ROOT / "3-PUBLISH"
    TEST_PUBLISH = PUBLISH / "TEST"
    
    ARCHIVE = _PIPELINE_ROOT / "0-ARCHIVE"

    FARM_IDS = DB / "Farm_IDs.db"
    FILE_IDS = DB / "File_IDs.db"


class DiscoveryNamespace():
    API_URI = r"https://discovery.nationalarchives.gov.uk/API"

    _closure_status = {
        'Closed Or Retained Document, Closed Description': "C",
        'Closed Or Retained Document, Open Description': "D",
        'Open Document, Open Description': "O",
        'Partially Closed… not currently used': "P",
    }
    UPDATE_SCOPE = {
        'new_record_with_digital_files': 'RecordAndReplica',
        'updated_digital_files': 'RecordAndReplica',
        'update_metadata_and_digital_files': 'RecordAndReplica',
        'new_metadata_only_record': 'RecordOnly',
        'update_metadata_not_digital_files': 'RecordOnly',
        'update_metadata_only_record': 'RecordOnly',
    }
    MAF32_RECORD_CONSTANTS = {
        'catalogueLevel': 8,
        'coveringFromDate': 19410101,
        'coveringToDate': 19431231,
        'chargeType': 1,
        'coveringDates': "1941-1943",
        'closureStatus': _closure_status['Open Document, Open Description'],
        'digitised': True,
        'heldBy': [
            {
                "xReferenceId": "A13530124",
                "xReferenceCode": "66",
                "xReferenceName": "The National Archives, Kew",
            }
        ],
        'legalStatus': "Public Record(s)",
        'source': "FS",
        'title': None,
    }
    MAF73_RECORD_CONSTANTS = {
        'coveringFromDate': 19410101,
        'coveringToDate': 19431231,
        'chargeType': 1,
        'coveringDates': "1941-1943",
        'closureStatus': _closure_status['Open Document, Open Description'],
        'digitised': True,
        'heldBy': [
            {
                "xReferenceId": "A13530124",
                "xReferenceCode": "66",
                "xReferenceName": "The National Archives, Kew",
            }
        ],
        'legalStatus': "Public Record(s)",
        'source': "FS",
        'title': None,
    }


PATH = PathNamespace()
REGEX = RegexNamespace()
DATA = DataNamespace()
CSVEXCEL = CSVandExcelNamespace()
DISCOVERY = DiscoveryNamespace()

