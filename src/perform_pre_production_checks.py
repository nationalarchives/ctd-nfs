import re

from containers import make_warnings_mapping

def perform_pre_production_checks(row_num: int, form: str, parish: str, filename1: str, filename2: str = None) -> str | dict:
    """
    Verify that values which identify the farm (forms, parish, box number, farm number) are consistent between the two filenames and the data in the spreadsheet row.
    If inconsistencies are found, raise ValueError with appropriate message.
    Checks preformed:
    * that filename matches the expected format
    * if two filenames provided, that they are consecutive (i.e. filename1 precedes filename2)
    * that parish number in filename matches parish number in spreadsheet
    * that box number in filename matches form number in spreadsheet
    * confirm form type is valid for filename(s) provided
    
    Args:
        row_num (int): row number from original csv, used for reporting errors/warning
        form (str): form number from spreadsheet row
        parish (str): parish number from spreadsheet row
        filename1 (str): first filename to check
        filename2 (str, optional): second filename to check. Defaults to None.

    Returns:
        str or dict: "Pass" or dictionary with warning messages for any issues found
    """

    warnings = make_warnings_mapping()

    RGX_FILENAMEPATTERN_FORM = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>0*\d+)\.tif$""")
    RGX_FILENAMEPATTERN_COVER = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)\.tif$""")
    RGX_FILENAMEPATTERN_OTHER = re.compile(r"""^MAF_*.*?\.tif$""")

    if rgxmatch := RGX_FILENAMEPATTERN_FORM.match(filename):
        return (rgxmatch['box_number'], rgxmatch['parish_number'], rgxmatch['image_number'], "")

    elif rgxmatch := RGX_FILENAMEPATTERN_COVER.match(filename):
        return (rgxmatch['box_number'], rgxmatch['parish_number'], 0, f"Row {row_num}: {filename} matches expected cover pattern. Error is this is not a cover.")
    
    elif rgxmatch := RGX_FILENAMEPATTERN.match(filename):
        return (rgxmatch['box_number'], rgxmatch['parish_number'], rgxmatch['image_number'], f"Row {row_num}: {filename} does not match expected pattern. Provisional values have been extracted to use in the reference but their accuracy cannot be guaranteed.")                       
    
    else:   
        raise ValueError(f"Row {row_num}: {filename} does not match expected pattern. Further checks on filenames could not be carried out and an accurate reference could not be generated.")
