"""
Verify that values which identify the farm (forms, parish, piece, farm number) are consistent between the two filenames and the data in the spreadsheet row.
If inconsistencies are found, raise ValueError with appropriate message.
Checks preformed:
* that filename matches the expected format
* if two filenames provided, that they are consecutive (i.e. filename_1 precedes filename_2)
* that parish number in filename matches parish number in spreadsheet
* that piece in filename matches form number in spreadsheet
* confirm form type is valid for filename(s) provided
"""
    
import re
from datetime import datetime

from src.farm_builder import initialise_forms_mapping, initialise_warnings_mapping
from src._config.custom_exceptions import FileNamePatternError
from src._config.constants import REGEX, DATA

def has_valid_reference_values(csv_values: dict, pattern_matches: dict[re.Match], row_prefix: str) -> bool:
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
        if key not in ['filename_1', 'filename_2','document_type', 'county', 'parish', ]
    ]
    
    checks = {
        f"Form type '{csv_values['document_type']}' is not a recognised form.": 
            lambda: csv_values['document_type'] not in valid_forms,
        
        f"filename_1 {csv_values['filename_1']} does not match expected pattern for form images or cover.": 
            lambda: not (pattern_matches['filename_1'] or pattern_matches['cover']),
        
        f"filename_2 {csv_values['filename_2']} does not match expected pattern for form images.":             
            lambda: csv_values['filename_2'] and not pattern_matches['filename_2'],

        f"{csv_values['filename_1']} and {csv_values['filename_2']} have valid form patterns but no farm data provided.":
            lambda: (csv_values['filename_2'] and pattern_matches['filename_2']) \
                and all(no_farm_details_provided)
    }
    
    errors = (msg for msg, check in checks.items() if check())
    if next(errors, None):
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
    
    filenames = f"{csv_values['filename_1']} and {csv_values['filename_2']}"
    if pattern_matches['filename_1']['piece'] != pattern_matches['filename_2']['piece']:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have different pieces.")

    parish_number = csv_values['parish'].split()[0]
    if pattern_matches['filename_1']['parish_number'] != pattern_matches['filename_2']['parish_number']:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have different parish numbers.")
    elif pattern_matches['filename_1']['parish_number'] != parish_number:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have a different parish number from parish name '{csv_values['parish']}'.")
       
    image1 = int(pattern_matches['filename_1']['image_number'])
    image2 = int(pattern_matches['filename_2']['image_number'])
    if image2 != image1 + 1:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} are either not consecutive images or in the wrong order.")
    
    return warnings


def report_cover_image_inconsistencies(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict, row_prefix: str) -> dict:
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

    file_is_cover_image = pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001"
    document_type_is_cover = csv_values['document_type'] == 'Cover'
    images_are_for_document_which_is_not_cover = \
        pattern_matches['filename_1'] and \
        pattern_matches['filename_1']['image_number'] != "0001" and \
        pattern_matches['filename_2']

    if images_are_for_document_which_is_not_cover and document_type_is_cover:
        warnings['Filename Warnings'].append(f"{row_prefix}Form type is 'Cover' but two form images were provided: {csv_values['filename_1']} and {csv_values['filename_2']}.")
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif document_type_is_cover and not file_is_cover_image:
        warnings['Filename Warnings'].append(f"{row_prefix}Form type is 'Cover' but {csv_values['filename_1']} does not match expected cover pattern or have image number 0001.")
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif not document_type_is_cover and file_is_cover_image:
        warnings['Filename Warnings'].append(f"{row_prefix}{csv_values['filename_1']} matches expected cover pattern or has image number 0001 but form type is '{csv_values['document_type']}'.")
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif document_type_is_cover and file_is_cover_image and csv_values['filename_2']:
        warnings['Filename Warnings'].append(f"{row_prefix}Form type is 'Cover', and {csv_values['filename_1']} matches expected pattern for cover image " \
                                             f"but additional image {csv_values['filename_2']} was also provided.")
        warnings['Type Warnings'].append(f"{row_prefix}document is listed as 'Cover' in data but two form images provided.")
    
    return warnings


def check_for_cover_with_farm_details(csv_values: dict, pattern_matches: dict[re.Match], warnings: dict, row_prefix: str) -> dict:
    file_is_cover_image = pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001"
    document_type_is_cover = csv_values['document_type'] == 'Cover'
    farm_details_provided = [
        item
        for key, item in csv_values.items() 
        if key not in ['filename_1', 'filename_2','document_type', 'county', 'parish', ]
    ]
    if (document_type_is_cover or file_is_cover_image) and any(farm_details_provided):
        warnings['Filename Warnings'].append(f"{row_prefix}Form type is 'Cover' but row contains farm details.")
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")
    
    return warnings 
    

def vali_dates(candi_date: str) -> str | None:    
    ''' Checks if the date, given as a string, is a valid date
    
        Key Arguments:
            potential_date - string containing the date value for checking
            
        Returns:
            warning/error message string if issues found, else None
    '''

    date_match: dict[re.Match] = {
        'daymonthyear': REGEX.DAYMONTHYEAR.match(candi_date),
        'monthyear': REGEX.MONTHYEAR.match(candi_date),
        'yearonly': REGEX.YEARONLY.match(candi_date),
        'ddmmyyyy': REGEX.DDMMYYYY.match(candi_date),
        'ddmonyyyy': REGEX.DDMONYEAR.match(candi_date),
    }

    date_type = (match_key for match_key in date_match.keys() if date_match[match_key])
    if not (date_type := next(date_type, None)):
        return f"[ERROR] '{candi_date}' is not a valid format. Further date checks cannot be performed."

    valid_year = REGEX.SURVEY_YEARS.match(date_match[date_type]['year'])
    if not valid_year:
        return f"[ERROR] '{candi_date}' is outside the survey timespan."

    candi_date = re.sub(r'[\/\-\. ]+', ' ', candi_date)
    if date_type in ['ddmmyyyy', 'ddmonyyyy']:
        day = date_match[date_type]['day'].zfill(2)
        if int(day) > 31:
            return f"[ERROR] '{candi_date}' is not a valid calendar date."

        month = date_match[date_type]['month']
        if date_type == 'ddmmyyyy':
            month = month.zfill(2)

        year = f"19{date_match[date_type]['year'][-2:]}"

        candi_date = f"{day} {month} {year}"

    for fmt in DATA.DATE_FORMATS:
        try:
            datetime.strptime(candi_date, fmt)
        except ValueError as ve:
            if "day is out of range for month" in str(ve):
                return f"[ERROR] '{candi_date}' is not a valid calendar date."
            else:
                continue


def validate_data(row_number, farm_data_row):
    pattern_matches: dict[re.Match] = {
            'filename_1': REGEX.FORM_PATTERN.match(farm_data_row['filename_1']),
            'filename_2': REGEX.FORM_PATTERN.match(farm_data_row['filename_2']),
            'cover': REGEX.COVER_PATTERN.match(farm_data_row['filename_1']),
        }

    row_prefix = f"Row {row_number}: "
    warnings: dict = initialise_warnings_mapping()

    try:
        has_valid_reference_values(farm_data_row, pattern_matches, row_prefix)
        check_for_cover_with_farm_details(farm_data_row, pattern_matches, warnings, row_prefix)
    except FileNamePatternError as e:
        # logger.info(f"{e}")
        raise

    if pattern_matches['filename_1'] and pattern_matches['filename_2']:
        warnings = check_values_between_filenames(farm_data_row, pattern_matches, warnings, row_prefix)

    if farm_data_row['document_type'] == 'Cover' or pattern_matches['cover'] or pattern_matches['filename_1']['image_number'] == "0001":
        warnings = report_cover_image_inconsistencies(farm_data_row, pattern_matches, warnings, row_prefix)

    for key in ['field_info_date', 'primary_record_date']:
        if not farm_data_row[key]:
            continue
        warning_key = 'Field Date Warnings' if key == 'field_info_date' else 'Primary Date Warnings'
        if check_result := vali_dates(farm_data_row[key]):
            warnings[warning_key].append(f"{row_prefix}{check_result}")

    return warnings
