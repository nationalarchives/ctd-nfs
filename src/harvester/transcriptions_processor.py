import re
from datetime import datetime

from src._dataclasses.farm_model import Form, ImageFile
from src._tools.constants import DATA, REGEX
from src._dataclasses.transcription_model import Transcription


class TranscriptionsProcessor:
    def __init__(self, transcriptions: list[Transcription]):
        self.transcriptions = transcriptions

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

    def _process_dates(self) -> dict[str, str]:        
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

    def _collate_attributes_for_further_processing(self) -> dict:
        transcription_fields = [
            'farm_name',
        	'addressee_title',
        	'addressee_individual_name',
        	'addressee_group_names',
        	'address',
        	'owner_title',
        	'owner_individual_name',
        	'owner_group_names',
        	'owner_address',
        	'farmer_title',
        	'farmer_individual_name',
        	'farmer_group_names',
        	'farmer_address',
        ]

        return {
            field_name: [
                getattr(transcription, field_name)
                for transcription in self.transcriptions
            ]
            for field_name in transcription_fields
        }
    
    def _collate_attributes_for_final_output(self) -> dict:
        collated_attributes = {
            'additional_farms': "",
            'acreage': "",
            'OS_map_sheet': "",
        }
            
        for field_name in collated_attributes:
            values = [
                getattr(transcription, field_name)
                for transcription in self.transcriptions
            ]
            collated_attributes[field_name] = "; ".join(values)

        return collated_attributes

    def _collate_forms(self) -> list[Form]:
        collated_forms: list[Form] = []

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
            collated_forms.append(Form(
                document_type=transcription.document_type, 
                images=image_files
                ))

        return collated_forms

    def process_transcriptions(self) -> dict:
        data_for_final_output = self._process_dates() | self._collate_attributes_for_final_output()
        return {
            'forms': self._collate_forms(),
            'for output': data_for_final_output,
            'for_processing': self._collate_attributes_for_further_processing(),
        }

