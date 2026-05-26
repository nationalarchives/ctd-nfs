import re
from datetime import datetime

from src._dataclasses.farm_model import Form, ImageFile
from src._tools.constants import DATA, REGEX
from src._dataclasses.transcription_model import Transcription


class TranscriptionsProcessor:
    def __init__(self, transcriptions: list[Transcription]):
        self.transcriptions = transcriptions

    def _check_for_multiple_B496(self) -> str | None:
        b496_forms = [
            "B496/EI"
            for transcription in self.transcriptions
            if transcription.document_type.name == "B496/EI"
        ]
        if len(b496_forms) > 1:
            return "Multiple B496/EI forms"

    def _collate_warnings(self) -> dict:
        farm_warnings = {}
        for transcription in self.transcriptions:
            if not transcription.warnings:
                continue
            for warning_type, warnings in transcription.warnings.items():
                if warning_type in warnings:
                    farm_warnings[warning_type].extend(warnings)
                else:
                    farm_warnings[warning_type] = warnings
        
        if b496_warning := self._check_for_multiple_B496():
            if 'Type Warnings' in farm_warnings:
                farm_warnings['Type Warnings'].append(b496_warning)
            else:
                farm_warnings['Type Warnings'] = [b496_warning]

        return farm_warnings

    def _normalize_date(self, candi_date: str) -> str:
        """Normalize date strings to a standard format day month year format e.g. 1 January 1941.
        Note: day must not have leading zeros.

        Args:
            date_str (str): The date string to normalize.

        Returns:
            str: The normalized date string.
        """

        if REGEX.MONTH.match(candi_date) or REGEX.MON.match(candi_date):
            if REGEX.MON.match(candi_date):
                index = DATA.ABBR_MONTH_NAMES.index(candi_date)
                candi_date = DATA.MONTH_NAMES[index]
            return f"{candi_date}"

        if REGEX.DAYMONTH.match(candi_date) or REGEX.DAYMON.match(candi_date):
            day, month = candi_date.split()
            if REGEX.DAYMON.match(candi_date):
                index = DATA.ABBR_MONTH_NAMES.index(month)
                month = DATA.MONTH_NAMES[index]
            return f"{int(day)} {month}"

        candi_date = REGEX.REMOVE_DELIMITERS.sub(' ', candi_date)
        date_match: dict[re.Match] = {
            'daymonthyear': REGEX.DAYMONTHYEAR.match(candi_date),
            'ddmmyyyy': REGEX.DDMMYYYY.match(candi_date),
        }
        if not (date_match['daymonthyear'] or date_match['ddmmyyyy']):
            return candi_date

        for fmt in DATA.DATE_FORMATS:
            try:
                parsed_date = datetime.strptime(candi_date, fmt)
                day, month, year = parsed_date.strftime("%d %B %Y").split()
                break
            except ValueError:
                continue

        return f"{int(day)} {month} {re.sub(r"^20", "19", year)}"

    def _collate_dates(self) -> dict[str, str]:        
        processed_dates = {
            'field_info_date': "",
            'primary_record_date': "",
        }
        for date_field in processed_dates:
            values = [
                getattr(transcription, date_field)
                for transcription in self.transcriptions
            ]
            normalized_dates = [
                self._normalize_date(date)
                for value in values
                for date in value.split(";")
            ]
            processed_dates[date_field] = "; ".join(normalized_dates)

        return processed_dates

    def _collate_non_date_attributes(self) -> dict:
        return {
            field_name: [
                getattr(transcription, field_name)
                for transcription in self.transcriptions
            ]
            for field_name in DATA.FARM_DATA_FIELDS
        }
    
    def _collate_forms(self) -> dict:
        collated_forms = {}

        for transcription in self.transcriptions:
            current_form_name = transcription.document_type.name
            if last_form := (collated_forms[-1] if collated_forms else None):
                is_same_form_name: bool = current_form_name == last_form.name
                is_consecutive: bool = (transcription.file1.image_number == last_form.images[-1].image_number + 1)

                if not transcription.file2 and is_same_form_name and is_consecutive:
                    collated_forms[-1].images.append(ImageFile(transcription.file1))
                    continue
            
            image_files = [
                ImageFile(file)
                for file in [transcription.file1, transcription.file2]
                if file
            ]

            collated_forms[current_form_name].append(image_files)

        return collated_forms

    def process_transcriptions(self) -> dict:
        data_for_final_output = self._process_dates() | self._collate_attributes_for_final_output()
        return {
            'forms': self._collate_forms(),
            'for output': data_for_final_output,
            'for_processing': self._collate_attributes_for_further_processing(),
        }

