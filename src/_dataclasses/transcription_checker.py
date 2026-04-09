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
import logging

from src._tools.constants import REGEX, DATA
from src._dataclasses.transcription_model import Transcription


logger = logging.getLogger(__name__)


def initialise_warnings_mapping() -> dict:
    """Create a mapping of warning categories to empty lists for storing warnings in the output file"""
    return {
        'Reference Warnings': [],
		'Filename Warnings': [],
		'Type Warnings': [],
		'Farm Number Warnings': [],
		'Farm Name Warnings': [],
		'Landowner Warnings': [],
		'Farmer Warnings': [],
		'Acreage Warnings': [],
		'Field Date Warnings': [],
		'Primary Date Warnings': []
    }


def check_for_cover_with_farm_details(transcription: Transcription, warnings: dict, row_prefix: str) -> dict:
    if (transcription.file1.is_cover) and (transcription.form_type.name == "Cover") and transcription.has_data:
        warnings['Filename Warnings'].append(f"{row_prefix}Form type is 'Cover' but row contains farm details.")
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")
    
    return warnings 


def report_cover_image_inconsistencies(transcription: Transcription, warnings: dict, row_prefix: str) -> dict:
    """
    Performs checks to ensure that if the form is a cover, only one image is provided and that it matches the cover pattern
    * if document type is 'Cover', only one image should be provided, and it should match either the cover pattern aor the form pattern with image number 0001
    i.e. no image number suffix in filename or image number is 0001

    Args:
        transcription (Transcription)

        warnings (dict): warning messages for any issues found

    Returns:
        warnings (dict):
    """

    if not transcription.file1.is_cover and transcription.file2 and transcription.form_type.name == "Cover":
        warnings['Filename Warnings'].append(
            f"{row_prefix}Form type is 'Cover' but two form images were provided: {transcription.file1.name} and {transcription.file2.name}."
        )
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif transcription.form_type.name == "Cover" and not transcription.file1.is_cover:
        warnings['Filename Warnings'].append(
            f"{row_prefix}Form type is 'Cover' but {transcription.file1.name} does not match expected cover pattern or have image number 0001."
        )
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif not transcription.form_type.name == "Cover" and transcription.file1.is_cover:
        warnings['Filename Warnings'].append(
            f"{row_prefix}{transcription.file1.name} matches expected cover pattern or has image number 0001 but form type is '{transcription.form_type.name}'."
        )
        warnings['Type Warnings'].append(f"{row_prefix}[see Filename Warnings]")

    elif transcription.form_type.name == "Cover" and transcription.file1.is_cover and transcription.file2:
        warnings['Filename Warnings'].append(
            f"{row_prefix}Form type is 'Cover', and {transcription.file1.name} matches expected pattern for cover image " \
            f"but additional image {transcription.file2.name} was also provided."
        )
        warnings['Type Warnings'].append(f"{row_prefix}document is listed as 'Cover' in data but two form images provided.")
    
    return warnings


def has_cover_issues(transcription: Transcription, row_prefix: str) -> dict | None:
    no_cover_warnings = initialise_warnings_mapping()

    warnings = check_for_cover_with_farm_details(transcription, no_cover_warnings, row_prefix)
    warnings = report_cover_image_inconsistencies(transcription, warnings, row_prefix)

    if warnings != no_cover_warnings:
        return warnings
    else:
        msg = f"{row_prefix}is a cover so will not be processed."
        logger.info(f" {msg:->80}")
        return None


def check_values_between_filenames(transcription: Transcription, warnings: dict, row_prefix: str) -> dict:
    """

    Performs checks on the piece, parish number and image number of the two file names
    * piece must be the same in the both file name
    * parish number must be the same in the both file name, and also match the number in the full parish name
    * image numbers must be consecutive

    Args:
        transcription (Transcription): 

        warnings (dict): warning messages for any issues found

    Returns:
        warnings (dict):
    """
    
    filenames = f"{transcription.file1.name} and {transcription.file2.name}"
    if transcription.file1.piece != transcription.file2.piece:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have different pieces.")

    parish_number = transcription.parish.split()[0]
    if transcription.file1.parish != transcription.file2.parish:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have different parish numbers.")
    elif transcription.file1.parish != parish_number:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} have a different parish number from parish name '{transcription.parish}'.")
       
    image1 = transcription.file1.image_number
    image2 = transcription.file2.image_number
    if image2 != image1 + 1:
        warnings['Filename Warnings'].append(f"{row_prefix}{filenames} are either not consecutive images or in the wrong order.")
    
    return warnings


def vali_dates(candi_date: str) -> str | None:    
    ''' Checks if the date, given as a string, is a valid date
    
        Key Arguments:
            potential_date - string containing the date value for checking
            
        Returns:
            warning/error message string if issues found, else None
    '''
    if candi_date == "[not specified]":
        return
    
    date_match: dict[re.Match] = {
        'daymonthyear': REGEX.DAYMONTHYEAR.match(candi_date),
        'monthyear': REGEX.MONTHYEAR.match(candi_date),
        'yearonly': REGEX.YEARONLY.match(candi_date),
        'ddmmyyyy': REGEX.DDMMYYYY.match(candi_date),
        'ddmonyyyy': REGEX.DDMONYEAR.match(candi_date),
        'daymonth': REGEX.DAYMONTH.match(candi_date),
        'daymon': REGEX.DAYMON.match(candi_date),
        'month': REGEX.MONTH.match(candi_date),
        'mon': REGEX.MON.match(candi_date),
    }

    date_type = (match_key for match_key in date_match.keys() if date_match[match_key])
    if not (date_type := next(date_type, None)):
        return f"[ERROR] '{candi_date}' is not a valid format. Further date checks cannot be performed."

    if date_match['month'] or date_match['mon']:
        return

    if date_type in ['daymonth', 'daymon']:
        day = date_match[date_type]['day'].zfill(2)
        month = date_match[date_type]['month']
        if (int(day) > 29 and month in ["February", "Feb"]) or int(day) > 31:
            return f"[ERROR] '{candi_date}' is not a valid calendar date."
        else:
            return

    valid_year = REGEX.SURVEY_YEARS.match(date_match[date_type]['year'])
    if not valid_year:
        return f"[ERROR] '{candi_date}' is outside the survey timespan."

    candi_date = re.sub(r'[\/\-\. ]+', ' ', candi_date)
    if date_type in ['daymonthyear', 'ddmmyyyy', 'ddmonyyyy']:
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


def check_for_other_row_data_issues(transcription: Transcription, warnings: dict, row_prefix: str):
    if transcription.file1.name and transcription.file2.name:
        warnings = check_values_between_filenames(transcription, warnings, row_prefix)

    for key in ['field_info_date', 'primary_record_date']:
        date_value = getattr(transcription, key)
        if not date_value:
            continue
        warning_key = 'Field Date Warnings' if key == 'field_info_date' else 'Primary Date Warnings'
        if check_result := vali_dates(date_value):
            warnings[warning_key].append(f"{row_prefix}{check_result}")

    return warnings


def run_validation_checks(transcription: Transcription, row_prefix) -> dict:
    warnings = initialise_warnings_mapping()
    
    if transcription.is_cover_page: 
        warnings = has_cover_issues(transcription, row_prefix)
        if warnings is None:
            continue
    
    warnings = check_for_other_row_data_issues(transcription, warnings, row_prefix)
