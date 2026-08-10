import dbm
import re
from collections import Counter
from datetime import UTC, datetime

from src._dataclasses.farm_model import ImageFile, ImageSet
from src._dataclasses.transcription_model import Filename, Transcription
from src._tools.constants import DATA, PATH, REGEX


class TranscriptionsProcessor:
    def __init__(self, transcriptions: list[Transcription]):
        self.transcriptions = transcriptions

    def _check_for_multiple_forms(self) -> str | None:
        form_totals = Counter([
            transcription.document_type.name
            for transcription in self.transcriptions
        ])
        warning = ""
        for form, total in form_totals.items():
            if total > 1:
                warning += f"Multiple {form} forms; "

        return warning or None

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
        
        if multiple_forms_warning := self._check_for_multiple_forms():
            if 'Type Warnings' in farm_warnings:
                farm_warnings['Type Warnings'].append(multiple_forms_warning)
            else:
                farm_warnings['Type Warnings'] = [multiple_forms_warning]

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
                parsed_date = datetime.strptime(candi_date, fmt).replace(tzinfo=UTC)
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
            date_values = [
                getattr(transcription, date_field)
                for transcription in self.transcriptions
            ]

            normalized_dates = []
            for value in date_values:
                if ";" in value:
                    normalized_items = [
                        self._normalize_date(_date)
                        for _date in re.split("; *", value)
                    ]
                    normalized_dates.append("; ".join(normalized_items))
                else:
                    normalized_dates.append(self._normalize_date(value))

            processed_dates[date_field] = normalized_dates

        return processed_dates

    def _collate_non_date_attributes(self) -> dict:
        return {
            field_name: [
                getattr(transcription, field_name)
                for transcription in self.transcriptions
                if field_name not in ['field_info_date', 'primary_record_date']
            ]
            for field_name in DATA.FARM_DATA_FIELDS
        }

    @staticmethod
    def _does_B496_have_3rd_image(file1: Filename, file2: Filename, last_image_set: ImageSet) -> bool:
        last_image = last_image_set[-1]
        is_consecutive: bool = (file1.image_number == last_image.image_number + 1)

        return (not file2 and is_consecutive)

    def _collate_forms(self) -> dict:
        collated_forms = {}

        for transcription in self.transcriptions:
            current_form_name = transcription.document_type.name
            if current_form_name not in collated_forms:
                collated_forms[current_form_name] = []

            if current_form_name == 'B496/EI' and \
                collated_forms['B496/EI'] and \
                self._does_B496_have_3rd_image(transcription.file1, transcription.file2, collated_forms['B496/EI'][-1]):
                    collated_forms[current_form_name][-1].append(ImageFile(transcription.file1))
                    continue
           
            image_set = [
                ImageFile(file)
                for file in [transcription.file1, transcription.file2]
                if file
            ]
            for index, image in enumerate(image_set):
                with dbm.open(PATH.FILE_IDS, 'c') as file_ids_db:
                    db_id = file_ids_db.get(image.name, "")
                    if db_id:
                        image_set[index].id = db_id.decode()
                    else:
                        file_ids_db[image.name] = image.id

            collated_forms[current_form_name].append(image_set)

        return collated_forms

    def process_transcriptions(self) -> dict:
        return {
            'forms': self._collate_forms(),
            'attributes': self._collate_non_date_attributes() | self._collate_dates(),
            'warnings': self._collate_warnings(),
        }

