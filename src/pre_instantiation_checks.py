import re

from farm_class_setup import make_warnings_mapping, make_forms_mapping


def perform_pre_instantiation_checks(csv_values: dict) -> str | dict:
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
        csv_values (dict): dictionary with the following keys
            row_num (int): row number from original csv, used for reporting errors/warning
            form (str): form number from spreadsheet row
            parish (str): parish number and name e.g. "1 Alkington"
            filename1 (str): front page of form
            filename2 (str, optional): back page of form Defaults to None, not used if form is Cover 

    Returns:
        str or dict: "Pass" or dictionary with warning messages for any issues found
    """

    RGX_FILENAMEPATTERN_FORM: re.Pattern = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    RGX_FILENAMEPATTERN_COVER: re.Pattern = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)\.tif$""")

    pattern_matches: dict[re.Match] = {
        'filename1': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename1']),
        'filename2': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename2']),
        'cover': RGX_FILENAMEPATTERN_COVER.match(csv_values['filename1']),
    }
    warnings: dict = make_warnings_mapping()

    if not pattern_matches['filename1']:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} does not match expected pattern for form images. " \
                                              f"Further checks on filenames could not be carried out and an accurate reference could not be generated."})

    if csv_values['filename2'] and not pattern_matches['filename2']:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename2']} does not match expected pattern for form images. " \
                                              f"Further checks on filenames could not be carried out and an accurate reference could not be generated."})
    
    if pattern_matches['filename1'] and pattern_matches['filename2']:
        warnings = check_values_between_filenames(csv_values, pattern_matches, warnings)

    if not csv_values['filename2'] and csv_values['form'] != 'Cover':
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"Form type is '{csv_values['form']}' but only one form image was provided: {csv_values['filename1']}."})

    if pattern_matches['filename1'].get('image_number', "") == "0001" and not csv_values['filename2'] and csv_values['form'] != 'Cover':
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} is image number 0001 which is usually a cover image. " \
                                              f"Form type is '{csv_values['form']}' but only one form image was provided."})
    
    if RGX_FILENAMEPATTERN_COVER.match(csv_values['filename1']) and csv_values['form'] != 'Cover':
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} matches cover pattern but form is {csv_values['form']}."})

    if RGX_FILENAMEPATTERN_COVER.match(csv_values['filename1']):
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} matches expected form for cover patterns. " \
                                              f"No further checks on this row performed."})

    if csv_values['form'] not in make_forms_mapping():
        warnings['Type Warnings'].append({f"Row {csv_values['row_num']}": f"Form type '{csv_values['form']}' is not a recognised form."})

    if warnings['Filename Warnings'] or warnings['Type Warnings']:
        return warnings
    
    return "Pass"


def check_values_between_filenames(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict) -> dict:
    """
    Performs checks on the box numbers, parish numbers and image numbers of the two file names
    * box numbers should be the same in the both file name
    * parish numbers should be the same in the both file name, and also match the number in the full parish name
    * image numbers must be consecutive

    Args:
        csv_values (dict): dictionary with the following keys
            'row_num' (int): row number from original csv, used for reporting errors/warning
            'form' (str): form number from spreadsheet row
            'parish' (str): parish number and name e.g. "1 Alkington"
            'filename1' (str): front page of form
            'filename2' (str, optional): back page of form Defaults to None, not used if form is Cover 

        pattern_matches
            'filename1' (re.Match): match for filename1 against form pattern
            'filename2' (re.Match): match for filename2 against form pattern
            'cover' (re.Match): match for filename1 against cover pattern

        warnings (dict): warning messages for any issues found

    Returns:
        warnings (dict):
    """

    if pattern_matches['filename1']['box_number'] != pattern_matches['filename2']['box_number']:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} and {csv_values['filename2']} have different box numbers. " \
                                                  f"Box number of {csv_values['filename1']} will be used in reference."})

    parish_number = csv_values['parish'].split()[0]
    if pattern_matches['filename1']['parish_number'] != pattern_matches['filename2']['parish_number']:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} and {csv_values['filename2']} have different parish numbers. " \
                                                  f"Number from full parish name: '{csv_values['parish']}' will be used in catalogue reference."})

    elif pattern_matches['filename1']['parish_number'] != parish_number:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} and {csv_values['filename2']} do not match value from parish name: '{parish_number}'. " \
                                                  f"Number from full parish name: '{csv_values['parish']}' will be used in catalogue reference."})
       
    image1 = int(pattern_matches['filename1']['image_number'])
    image2 = int(pattern_matches['filename2']['image_number'])
    if image2 != image1 + 1:
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"{csv_values['filename1']} and {csv_values['filename2']} are not consecutive images."})

    if csv_values['form'] == 'Cover':
        warnings['Filename Warnings'].append({f"Row {csv_values['row_num']}": f"Form type is 'Cover' but two form images were provided: {csv_values['filename1']} and {csv_values['filename2']}."})

    return warnings


