import re

from src.farm_class_setup import make_warnings_mapping, make_forms_mapping


def perform_pre_instantiation_checks(csv_values: dict) -> str | dict:
    """
    Verify that values which identify the farm (forms, parish, box number, farm number) are consistent between the two filenames and the data in the spreadsheet row.
    If inconsistencies are found, raise ValueError with appropriate message.
    Checks preformed:
    * that filename matches the expected format
    * if two filenames provided, that they are consecutive (i.e. filename_1 precedes filename_2)
    * that parish number in filename matches parish number in spreadsheet
    * that box number in filename matches form number in spreadsheet
    * confirm form type is valid for filename(s) provided
    
    Args:
        csv_values (dict): dictionary with the following keys
            row_num (int): row number from original csv, used for reporting errors/warning
            document_type (str): form number from spreadsheet row
            parish (str): parish number and name e.g. "1 Alkington"
            filename_1 (str): front page of form
            filename_2 (str, optional): back page of form Defaults to None, not used if form is Cover 

    Returns:
        str or dict: "Pass" or dictionary with warning messages for any issues found
    """

    RGX_FILENAMEPATTERN_FORM: re.Pattern = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    RGX_FILENAMEPATTERN_COVER: re.Pattern = re.compile(r"""^MAF32-(?P<box_number>\d+)[-_](?P<parish_number>\d+)\.tif$""")

    pattern_matches: dict[re.Match] = {
        'filename_1': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename_1']),
        'filename_2': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename_2']),
        'cover': RGX_FILENAMEPATTERN_COVER.match(csv_values['filename_1']),
    }
    warnings: dict = make_warnings_mapping()

    if not pattern_matches['filename_1']:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} does not match expected pattern for form images. " \
                                              f"Further checks on filenames could not be carried out and an accurate reference could not be generated.")

    if csv_values['filename_2'] and not pattern_matches['filename_2']:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_2']} does not match expected pattern for form images. " \
                                              f"Further checks on filenames could not be carried out and an accurate reference could not be generated.")
        return warnings
    
    if pattern_matches['filename_1'] and pattern_matches['filename_2']:
        warnings = check_values_between_filenames(csv_values, pattern_matches, warnings)

    warnings = check_cover_image_consistency(csv_values, pattern_matches, warnings)

    if csv_values['document_type'] not in make_forms_mapping():
        warnings['Type Warnings'].append(f"Row {csv_values['row_num']}: Form type '{csv_values['document_type']}' is not a recognised form.")

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
            'document_type' (str): form number from spreadsheet row
            'parish' (str): parish number and name e.g. "1 Alkington"
            'filename_1' (str): front page of form
            'filename_2' (str, optional): back page of form Defaults to None, not used if form is Cover 

        pattern_matches
            'filename_1' (re.Match): match for filename_1 against form pattern
            'filename_2' (re.Match): match for filename_2 against form pattern
            'cover' (re.Match): match for filename_1 against cover pattern

        warnings (dict): warning messages for any issues found

    Returns:
        warnings (dict):
    """

    if pattern_matches['filename_1']['box_number'] != pattern_matches['filename_2']['box_number']:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} and {csv_values['filename_2']} have different box numbers. " \
                                                  f"Box number of {csv_values['filename_1']} will be used in the catalogue reference.")

    parish_number = csv_values['parish'].split()[0]
    if pattern_matches['filename_1']['parish_number'] != pattern_matches['filename_2']['parish_number']:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} and {csv_values['filename_2']} have different parish numbers. " \
                                                  f"Parish number from full parish name '{csv_values['parish']}' will be used in the catalogue reference.")

    elif pattern_matches['filename_1']['parish_number'] != parish_number:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} and {csv_values['filename_2']} have a diffeent parish number from parish name '{csv_values['parish']}'. " \
                                                  f"Parish number from full parish name will be used in the catalogue reference.")
       
    image1 = int(pattern_matches['filename_1']['image_number'])
    image2 = int(pattern_matches['filename_2']['image_number'])
    if image2 != image1 + 1:
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} and {csv_values['filename_2']} are either not consecutive images or in the wrong order.")

    if csv_values['document_type'] == 'Cover':
        warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: Form type is 'Cover' but two form images were provided: {csv_values['filename_1']} and {csv_values['filename_2']}.")
        warnings['Type Warnings'].append(f"Row {csv_values['row_num']}: [see Filename Warnings]")
    
    return warnings


def check_cover_image_consistency(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict) -> dict:
    """
    Performs checks to ensure that if the form is a cover, only one image is provided and that it matches the cover pattern 
    i.e. no image number suffix in filename or image number is 0001

    Args:
        csv_values (dict): dictionary with the following keys
            row_num (int): row number from original csv, used for reporting errors/warning
            form (str): form number from spreadsheet row
            parish (str): parish number and name e.g. "1 Alkington"
            filename_1 (str): front page of form
            filename_2 (str, optional): back page of form Defaults to None, not used if form is Cover 

        pattern_matches
            'filename_1' (re.Match): match for filename_1 against form pattern
            'filename_2' (re.Match): match for filename_2 against form pattern
            'cover' (re.Match): match for filename_1 against cover pattern

        warnings (dict): warning messages for any issues found

    Returns:
        warnings (dict):
    """
    image_number_is_cover = pattern_matches['filename_1']['image_number'] == "0001"
    cover_is_form = csv_values['document_type'] == 'Cover'
    
    if not cover_is_form:
        if image_number_is_cover:
            warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} is image number 0001 which is expected to be a cover image,+ " \
                                                   f"but form type is '{csv_values['document_type']}'.")
            warnings['Type Warnings'].append(f"'{csv_values['document_type']}' in data but only one form image was provided.")
    
        elif pattern_matches['cover']:
            warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: {csv_values['filename_1']} matches cover pattern but form type is '{csv_values['document_type']}'.")
            warnings['Type Warnings'].append(f"Row {csv_values['row_num']}: [see Filename Warnings]")
    else:
        if not pattern_matches['cover']:
            warnings['Filename Warnings'].append(f"Row {csv_values['row_num']}: Form type is 'Cover' but {csv_values['filename_1']} does not match expected cover pattern.")
            warnings['Type Warnings'].append(f"Row {csv_values['row_num']}: [see Filename Warnings]")
    
    if pattern_matches['cover'] and csv_values['filename_2']:
        warnings['Filename Wiarnings'].append(f"Row {csv_values['row_num']}: Form type is '{csv_values['document_type']}', and {csv_values['filename_1']} matches expected pattern for cover image " \
                                               f"but additional image {csv_values['filename_2']} was also provided.")
        warnings['Type Warnings'].append(f"Row {csv_values['row_num']}: [see Filename Warnings]")
    
    return warnings
