"""
module for defining constants and constant namespaces.
"""

from pathlib import Path


EXCEL_LOOKUP_FILE = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\MAF 32 Piece Lookup Table 04-12-2025.xlsx")
DB_FILE = Path("MAF 32 Piece Lookup Table.db")


class DataFolders():
    __slots__ = ()

    _root = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline")
    LOOKUP_TABLE = _root / "0-DB" / DB_FILE
    INPUT = _root / "1-INPUT"
    TRANSFORM = _root / "3-TRANSFORM"
    ARCHIVE = _root / "4-ARCHIVE"
    OUTPUT = _root / "5-OUTPUT"


DATA = DataFolders()

