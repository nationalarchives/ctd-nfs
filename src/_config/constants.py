"""
module for defining constants and constant namespaces.
"""

from pathlib import Path
import re
import shelve


EXCEL_LOOKUP_FILE = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\MAF 32 Piece Lookup Table 04-12-2025.xlsx")
_root = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline")
    
_PIECE_LOOKUP_DB = Path("MAF 32 Piece Lookup Table.db")

class RegexPatterns():
    __slots__ = ()

    FORM_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    COVER_PATTERN = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)\.tif$""")


class DataFolders():
    __slots__ = ()

    with shelve.open(Path.joinpath(_root, "0-DB", _PIECE_LOOKUP_DB), "c") as shelf:
        PIECE_LOOKUP_TABLE = shelf['pieces lookup table']    
    INPUT = _root / "1-INPUT"
    TRANSFORM = _root / "3-TRANSFORM"
    ARCHIVE = _root / "4-ARCHIVE"
    OUTPUT = _root / "5-OUTPUT"


DATA = DataFolders()
REGEX = RegexPatterns()

