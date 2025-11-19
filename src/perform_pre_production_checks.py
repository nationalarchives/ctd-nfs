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
        parish (str): parish number and name e.g. "1 Alkington"
        filename1 (str): first filename to check
        filename2 (str, optional): second filename to check. Defaults to None.

    Returns:
        str or dict: "Pass" or dictionary with warning messages for any issues found
    """

    parish_number = parish.split()[0]
    RGX_FILENAMEPATTERN_FORM = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>0*\d+)\.tif$""")
    RGX_FILENAMEPATTERN_COVER = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)\.tif$""")
    RGX_FILENAMEPATTERN_OTHER = re.compile(r"""^MAF_*.*?\.tif$""")

    warnings = make_warnings_mapping()
    if not (filename1_match := RGX_FILENAMEPATTERN_FORM.match(filename1)):
        warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} does not match expected pattern for form images. Further checks on filenames could not be carried out and an accurate reference could not be generated."})

    if filename2 and not (filename2_match := RGX_FILENAMEPATTERN_FORM.match(filename2)):
        warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename2} does not match expected pattern for form images. Further checks on filenames could not be carried out and an accurate reference could not be generated."})
    
    if filename1_match and filename2_match:
        if filename1_match['box_number'] != filename2_match['box_number']:
            warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} and {filename2} have different box numbers. Box number of {filename1} will be used in reference."})

        if filename1_match['parish_number'] != filename2_match['parish_number']:
            warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} and {filename2} have different parish numbers. Number from full parish name: '{parish}' will be used in catalogue reference."})

        elif filename1_match['parish_number'] != parish_number:
            warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} and {filename2} do not match value from parish name: '{parish_number}'. Number from full parish name: '{parish}' will be used in catalogue reference."})
       
        image1 = int(filename1_match['image_number'])
        image2 = int(filename2_match['image_number'])
        if image2 != image1 + 1:
            warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} and {filename2} are not consecutive images."})

        if form == 'Cover':
            warnings['Filename Warnings'].append({f"Row {row_num}": f"Form type is 'Cover' but two form images were provided: {filename1} and {filename2}."})

    if not filename2 and form != 'Cover':
        warnings['Filename Warnings'].append({f"Row {row_num}": f"Form type is '{form}' but only one form image was provided: {filename1}."})

    if RGX_FILENAMEPATTERN_COVER.match(filename1) and form != 'Cover':
        warnings['Filename Warnings'].append({f"Row {row_num}": f"{filename1} matches cover pattern but form is not a Cover."})

    if RGX_FILENAMEPATTERN_OTHER.match(filename2) and form != 'Cover':
        pass

    # if rgxmatch := RGX_FILENAMEPATTERN_FORM.match(filename):
    #     return (rgxmatch['box_number'], rgxmatch['parish_number'], rgxmatch['image_number'], "")

    # elif rgxmatch := RGX_FILENAMEPATTERN_COVER.match(filename):
    #     return (rgxmatch['box_number'], rgxmatch['parish_number'], 0, f"Row {row_num}: {filename} matches expected cover pattern. Error is this is not a cover.")
    
    # elif rgxmatch := RGX_FILENAMEPATTERN.match(filename):
    #     return (rgxmatch['box_number'], rgxmatch['parish_number'], rgxmatch['image_number'], f"Row {row_num}: {filename} does not match expected pattern. Provisional values have been extracted to use in the reference but their accuracy cannot be guaranteed.")                       
    
    # else:   
    #     raise ValueError(f"Row {row_num}: {filename} does not match expected pattern. Further checks on filenames could not be carried out and an accurate reference could not be generated.")
