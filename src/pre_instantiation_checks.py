"""
Pre-instantiation checks to ensure that farm identifying values are consistent between filenames and spreadsheet data.
1: invalid form type
        can be ignored as we already check for these before running it through the merger so any that remain ought to be correct

2: either filename is invalid
        We would like warnings

3: piece numbers or parish numbers don't match between filenames
        We would like warnings

4: parish number in filenames doesn't match number in parish name
        We would like warnings

5: images not consecutive
        can be ignored as we already check for these before running it through the merger so any that remain ought to be correct

6: form type is Cover but the filename_1 doesn't have a cover pattern (and vice versa)
        We would like warnings

7: form type is Cover but two filenames provided
        we would like a warning if the form type is cover and there are two filenames paired with each other
        
8: valid filenames but form is Cover
        this can probably also be ignored, my understanding is that covers will be ignored in the final upload, but probably best not to reject the row at this point
"""

import re

from farm_class_setup import initialise_forms_mapping, initialise_warnings_mapping


def perform_pre_instantiation_checks(csv_values: dict) -> dict:
    """
    Verify that values which identify the farm (forms, parish, piece, farm number) are consistent between the two filenames and the data in the spreadsheet row.
    If inconsistencies are found, raise ValueError with appropriate message.
    Checks preformed:
    * that filename matches the expected format
    * if two filenames provided, that they are consecutive (i.e. filename_1 precedes filename_2)
    * that parish number in filename matches parish number in spreadsheet
    * that piece in filename matches form number in spreadsheet
    * confirm form type is valid for filename(s) provided
    
    Args:
        csv_values (dict): dictionary with the following keys
            row_number (int): row number from original csv, used for reporting errors/warning
            document_type (str): form number from spreadsheet row
            parish (str): parish number and name e.g. "1 Alkington"
            filename_1 (str): front page of form
            filename_2 (str, optional): back page of form Defaults to None, not used if form is Cover 

    Returns:
        dict: the piece, parish number & document_type (for later use to generate the catalogue & farm references), and warning messages for any issues found
    """

    RGX_FILENAMEPATTERN_FORM: re.Pattern = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)_+(?P<image_number>\d+)\.tif$""")
    RGX_FILENAMEPATTERN_COVER: re.Pattern = re.compile(r"""^MAF32-(?P<piece>\d+)[-_](?P<parish_number>\d+)\.tif$""")

    pattern_matches: dict[re.Match] = {
        'filename_1': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename_1']),
        'filename_2': RGX_FILENAMEPATTERN_FORM.match(csv_values['filename_2']),
        'cover': RGX_FILENAMEPATTERN_COVER.match(csv_values['filename_1']),
    }
    row = f"Row {csv_values['row_number']}: "
    
    if validate_farm_reference_values(csv_values, pattern_matches):
        raise ValueError(f"{row} rejected due to errors in data.")    

    
    warnings: dict = initialise_warnings_mapping()
    if pattern_matches['filename_1'] and pattern_matches['filename_2']:
        warnings = check_values_between_filenames(csv_values, pattern_matches, warnings)

    if csv_values['document_type'] == 'Cover' or pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001":
        warnings = check_cover_image_consistency(csv_values, pattern_matches, warnings) 

    return warnings


def validate_farm_reference_values(csv_values: dict, pattern_matches: dict[re.Match], row_prefix: str) -> bool:
    """
    Perform checks which will result in the row being rejected if they fail
    * invalid form type
    * either filename is invalid
    * images not consecutive

    Args:
        csv_values (dict): dictionary with the following keys

    Returns:
        bool: True if row should be rejected, False otherwise
    """
    valid_forms = list(initialise_forms_mapping().keys())
    no_farm_details_provided = [
        item == ""
        for key, item in csv_values.items() 
        if key not in ['row_number', 'document_type', 'parish', 'filename_1', 'filename_2']
    ]
    
    rules = {
        f"Form type '{csv_values['document_type']}' is not a recognised form.": 
            lambda: csv_values['document_type'] not in valid_forms,
        
        f"{csv_values['filename_1']} does not match expected pattern for form images or cover.": 
            lambda: not (pattern_matches['filename_1'] or pattern_matches['cover']),
        
        f"{csv_values['filename_2']} does not match expected pattern for form images. ":             
            lambda: csv_values['filename_2'] and not pattern_matches['filename_2'],

        f"{csv_values['filename_1']} and {csv_values['filename_2']} have valid form patterns but no farm data provided.":
            lambda: (csv_values['filename_2'] and pattern_matches['filename_2']) \
                and all(no_farm_details_provided)
    }
    
    errors = (msg for msg, check in rules.items() if check())
    if error_messaage := next(errors, None):
        print(f"{row_prefix} will be rejected: {error_messaage}")
        return False
    
    return True


def check_values_between_filenames(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict, row_prefix: str) -> dict:
    """
    Performs checks on the piece, parish number and image number of the two file names
    * piece must be the same in the both file name
    * parish number must be the same in the both file name, and also match the number in the full parish name
    * image numbers must be consecutive

    Args:
        csv_values (dict): dictionary with the following keys
            'row_number' (int): row number from original csv, used for reporting errors/warning
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
    if pattern_matches['filename_1']['piece'] != pattern_matches['filename_2']['piece']:
        warnings['Filename Warnings'].append(f"{row_prefix}{csv_values['filename_1']} and {csv_values['filename_2']} have different pieces.")

    parish_number = csv_values['parish'].split()[0]
    if pattern_matches['filename_1']['parish_number'] != pattern_matches['filename_2']['parish_number']:
        warnings['Filename Warnings'].append(f"{row_prefix}{csv_values['filename_1']} and {csv_values['filename_2']} have different parish numbers.")
    elif pattern_matches['filename_1']['parish_number'] != parish_number:
        warnings['Filename Warnings'].append(f"{row_prefix}{csv_values['filename_1']} and {csv_values['filename_2']} have a different parish number from parish name '{csv_values['parish']}'.")
       
    image1 = int(pattern_matches['filename_1']['image_number'])
    image2 = int(pattern_matches['filename_2']['image_number'])
    if image2 != image1 + 1:
        warnings['Filename Warnings'].append(f"{row_prefix}{csv_values['filename_1']} and {csv_values['filename_2']} are either not consecutive images or in the wrong order.")
    
    return warnings


def check_cover_image_consistency(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict) -> dict:
    """
    Performs checks to ensure that if the form is a cover, only one image is provided and that it matches the cover pattern
    * if document type is 'Cover', only one image should be provided, and it should match either the cover pattern aor the form pattern with image number 0001
    i.e. no image number suffix in filename or image number is 0001

    Args:
        csv_values (dict): dictionary with the following keys
            row_number (int): row number from original csv, used for reporting errors/warning
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
    row = f"Row {csv_values['row_number']}: "

    file_is_cover_image = pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001"
    document_type_is_cover = csv_values['document_type'] == 'Cover'
    images_are_for_document_which_is_not_cover = \
        pattern_matches['filename_1'] and \
        pattern_matches['filename_1']['image_number'] != "0001" and \
        pattern_matches['filename_2']

    if document_type_is_cover and not file_is_cover_image:
        warnings['Filename Warnings'].append(f"{row}Form type is 'Cover' but {csv_values['filename_1']} does not match expected cover pattern or have image number 0001.")
        warnings['Type Warnings'].append(f"{row}[see Filename Warnings]")

    if not document_type_is_cover and file_is_cover_image:
        warnings['Filename Warnings'].append(f"{row}{csv_values['filename_1']} matches expected cover pattern or has image number 0001 but form type is '{csv_values['document_type']}'.")
        warnings['Type Warnings'].append(f"{row}[see Filename Warnings]")

    if document_type_is_cover and file_is_cover_image and csv_values['filename_2']:
        warnings['Filename Warnings'].append(f"{row}Form type is 'Cover', and {csv_values['filename_1']} matches expected pattern for cover image " \
                                             f"but additional image {csv_values['filename_2']} was also provided.")
        warnings['Type Warnings'].append(f"{row}document is listed as 'Cover' in data but two form images provided.")

    if images_are_for_document_which_is_not_cover and document_type_is_cover:
        warnings['Filename Warnings'].append(f"{row}Form type is 'Cover' but two form images were provided: {csv_values['filename_1']} and {csv_values['filename_2']}.")
        warnings['Type Warnings'].append(f"{row}[see Filename Warnings]")
    
    return warnings


def confirm_row_is_not_cover(csv_values: dict, pattern_matches: dict[re.Match], row_prefix: str) -> bool:
    file_is_cover_image = pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001"
    document_type_is_cover = csv_values['document_type'] == 'Cover'
    no_farm_details_provided = [
        item == ""
        for key, item in csv_values.items() 
        if key not in ['row_number', 'document_type', 'parish', 'filename_1', 'filename_2']
    ]
    if (document_type_is_cover or file_is_cover_image) and all(no_farm_details_provided):
        print(f"{row_prefix} skipped as Cover with no farm data provided.")
        return False
    
    return True 

