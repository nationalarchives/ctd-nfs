"""
module for defining constants and constant namespaces.
"""

from pathlib import Path
import re
import shelve


EXCEL_LOOKUP_FILE = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\MAF 32 Piece Lookup Table 04-12-2025.xlsx")
_PIPELINE_ROOT = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline")
    
_PIECE_LOOKUP_DB = Path("MAF 32 Piece Lookup Table.db")
_FARMS_CACHE = Path("MAF 32 Farms.db")

class RegexPatterns():
    __slots__ = ()

    COUNTY_NAME = re.compile(r"""^(?P<county_name>[A-Z\s\(\)]+)+.*?$""")
    FORM_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    COVER_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)\.tif$""")


class DataFolders():
    __slots__ = ()

    with shelve.open(Path.joinpath(_PIPELINE_ROOT, "0-DB", _PIECE_LOOKUP_DB), "c") as shelf:
        PIECE_LOOKUP_TABLE = shelf['pieces lookup table']    
    with shelve.open(Path.joinpath(_PIPELINE_ROOT, "0-DB", _FARMS_CACHE), "c") as shelf:
        FARMS_DB = shelf['farms db']    
    INPUT = _PIPELINE_ROOT / "1-INPUT"
    TRANSFORM = _PIPELINE_ROOT / "3-TRANSFORM"
    ARCHIVE = _PIPELINE_ROOT / "4-ARCHIVE"
    OUTPUT = _PIPELINE_ROOT / "5-OUTPUT"


DATA = DataFolders()
REGEX = RegexPatterns()

