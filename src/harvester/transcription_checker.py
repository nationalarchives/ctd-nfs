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
    
import logging
import re
from datetime import UTC, datetime

from src._dataclasses.transcription_model import Transcription
from src._tools.constants import DATA, REGEX

logger = logging.getLogger(__name__)


class TranscriptionChecker:
    def __init__(self, transcription, row_number):
        self.transcription: Transcription = transcription
        self.row_prefix = f"Row {row_number}: "
        self.warnings = {
                'Reference Warnings': [],
                'Filename Warnings': [],
                'Type Warnings': [],
                'Field Date Warnings': [],
                'Primary Date Warnings': []
            }

    def _check_for_cover_with_farm_details(self) -> None:
        if (self.transcription.file1.is_cover) and (self.transcription.document_type.name == "Cover") and self.self.transcription.has_data:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}Form type is 'Cover' but row contains farm details.")
            self.warnings['Type Warnings'].append(f"{self.row_prefix}[see Filename Warnings]")

    def _report_cover_image_inconsistencies(self) -> None:
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

        if not self.transcription.file1.is_cover and self.transcription.file2 and self.transcription.document_type.name == "Cover":
            self.warnings['Filename Warnings'].append(
                f"{self.row_prefix}Form type is 'Cover' but two form images were provided: {self.transcription.file1.name} and {self.transcription.file2.name}."
            )
            self.warnings['Type Warnings'].append(f"{self.row_prefix}[see Filename Warnings]")

        elif self.transcription.document_type.name == "Cover" and not self.transcription.file1.is_cover:
            self.warnings['Filename Warnings'].append(
                f"{self.row_prefix}Form type is 'Cover' but {self.transcription.file1.name} does not match expected cover pattern or have image number 0001."
            )
            self.warnings['Type Warnings'].append(f"{self.row_prefix}[see Filename Warnings]")

        elif self.transcription.document_type.name != "Cover" and self.transcription.file1.is_cover:
            self.warnings['Filename Warnings'].append(
                f"{self.row_prefix}{self.transcription.file1.name} matches expected cover pattern or has image number 0001 but form type is '{self.transcription.document_type.name}'."
            )
            self.warnings['Type Warnings'].append(f"{self.row_prefix}[see Filename Warnings]")

        elif self.transcription.document_type.name == "Cover" and self.transcription.file1.is_cover and self.transcription.file2:
            self.warnings['Filename Warnings'].append(
                f"{self.row_prefix}Form type is 'Cover', and {self.transcription.file1.name} matches expected pattern for cover image " \
                f"but additional image {self.transcription.file2.name} was also provided."
            )
            self.warnings['Type Warnings'].append(f"{self.row_prefix}document is listed as 'Cover' in data but two form images provided.")

    def _has_cover_issues(self) -> None:
        self._check_for_cover_with_farm_details()
        self._report_cover_image_inconsistencies()

        msg = f"{self.row_prefix}is a cover so will not be processed."
        logger.info(f" {msg:->80}")

    def _check_values_between_filenames(self) -> None:
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
        
        filenames = f"{self.transcription.file1.name} and {self.transcription.file2.name}"
        if self.transcription.file1.piece != self.transcription.file2.piece:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{filenames} have different pieces.")

        parish_number = self.transcription.parish.split()[0]
        if self.transcription.file1.parish_number != self.transcription.file2.parish_number:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{filenames} have different parish numbers.")
        elif self.transcription.file1.parish_number != parish_number:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{filenames} have a different parish number from parish name '{self.transcription.parish}'.")
        
        image1 = self.transcription.file1.image_number
        image2 = self.transcription.file2.image_number
        if image2 != image1 + 1:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{filenames} are either not consecutive images or in the wrong order.")
        """

    def _check_filename_values_against_catalogue_reference(self) -> None:
        if self.transcription.file1.piece != self.transcription.piece:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{self.transcription.file1.name} piece value does not match the catalogue reference.")

        if self.transcription.file1.parish_number != self.transcription.parish_number:
            self.warnings['Filename Warnings'].append(f"{self.row_prefix}{self.transcription.file1.name} parish number does not match the catalogue reference.")

    @staticmethod
    def _vali_dates(candi_date: str) -> str | None:    
        ''' Checks if the date, given as a string, is a valid date
        
            Key Arguments:
                potential_date - string containing the date value for checking
                
            Returns:
                warning/error message string if issues found, else None
        '''
        if candi_date in ["_null_", "_not transcribed_"]:
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

        date_type = (match_key for match_key in date_match if date_match[match_key])
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
                datetime.strptime(candi_date, fmt).replace(tzinfo=UTC)
            except ValueError as ve:
                if "day is out of range for month" in str(ve):
                    return f"[ERROR] '{candi_date}' is not a valid calendar date."
                else:
                    continue

    def _check_for_other_row_data_issues(self) -> None:
        if self.transcription.file1.name and self.transcription.file2.name:
            self._check_values_between_filenames()

        for key in ['field_info_date', 'primary_record_date']:
            date_value = getattr(self.transcription, key)
            if date_value == "_null_":
                continue
            warning_key = 'Field Date Warnings' if key == 'field_info_date' else 'Primary Date Warnings'
            if check_result := self._vali_dates(date_value):
                self.warnings[warning_key].append(f"{self.row_prefix}{check_result}")

    def run_validation_checks(self) -> dict | None:
        if self.transcription.is_cover_page: 
            self._has_cover_issues()
        
        if self.transcription.file2:
            self._check_for_other_row_data_issues()

        return self.warnings if any(value for value in self.warnings.values() if value) else None
    
