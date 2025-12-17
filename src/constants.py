"""
module for defining constants and constant namespaces.
"""

from pathlib import Path
import shelve
from collections import OrderedDict

from read_db_cache import LOOKUP_TABLE_DB


EXCEL_LOOKUP_FILE = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\MAF 32 Piece Lookup Table 04-12-2025.xlsx")
DB_FILE = Path("MAF 32 Piece Lookup Table.db")


class FarmSetup():
    __slots__ = ()
    FORMS_MAP = OrderedDict([
        ('C 47/SSY', []),
        ('C 49/SSY', []),
        ('C51/SSY', []),
        ('SF', []),
        ('SF C69/SSY', []),
        ('B496/EI', []),
        ('Other', []),
        ('Cover', []),
    ])


class DataFolders():
    __slots__ = ()

    _root = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline")
    
    _db = _root / "0-DB" / DB_FILE
    with shelve.open(_db, "c") as shelf:
        LOOKUP_TABLE = shelf['pieces lookup table']    
    INPUT = _root / "1-INPUT"
    TRANSFORM = _root / "3-TRANSFORM"
    ARCHIVE = _root / "4-ARCHIVE"
    OUTPUT = _root / "5-OUTPUT"


DATA = DataFolders()
FARM_SETUP = FarmSetup()

