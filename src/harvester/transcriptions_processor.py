import re
from datetime import datetime
from dataclasses import dataclass

from src._dataclasses.farm_model import Farm
from src._tools.constants import DATA, REGEX
from src._dataclasses.transcription_model import Transcription


@dataclass
class Details:
    name: str
    address: str


class TranscriptionsProcessor:
    def __init__(self, transcriptions: list):
        self.transcription: Transcription = transcription

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

    def _concatenate_attribute_values(self, existing_value: str, new_value: str) -> str:
        """Concatenate two values, ensuring no duplicates.

        Args:
            existing_value (str): The existing value.
            new_value (str): The new value to be added.

        Returns:
            The concatenated value with duplicates removed.
        """
        if type(existing_value) is str and type(new_value) is str:
            return [existing_value, new_value]

        if type(existing_value) is str and type(new_value) is list:
            return [existing_value] + new_value

        if type(existing_value) is list and type(new_value) is str:
            return existing_value + [new_value]

        if type(existing_value) is list and type(new_value) is list:
            return existing_value + new_value

    def _concatenate_instance_attributes(self, existing_attribute: str, new_attribute: str, field_name: str) -> None:
        existing_value = getattr(existing_attribute, field_name)
        new_value = getattr(new_attribute, field_name)

        concatenated_value = self.concatenate_attribute_values(existing_value, new_value)
        setattr(existing_attribute, field_name, concatenated_value)

    def _concatenate_instance(self, existing_farm: 'Farm', new_farm: 'Farm') -> 'Farm':
        """
        Concatenate the attributes of two Farm instances, ensuring no duplicates.

        Args:
            existing_farm (Farm): _description_
            new_farm (Farm): _description_

        Returns:
            Farm: _description_
        """
        for field_name in existing_farm.__dict__:
            if field_name in ['addressee', 'owner', 'farmer']:
                existing_detail = getattr(existing_farm, field_name)
                new_detail = getattr(new_farm, field_name)
                for detail_attribute in ['title', 'individual_name', 'group_names', 'address']:
                    self.concatenate_instance_attributes(existing_detail, new_detail, detail_attribute)

            if field_name in ['additional_farms', 'farm_name', 'acreage', 'OS_map_sheet']:
                self.concatenate_instance_attributes(existing_farm, new_farm, field_name)

        existing_farm.forms = self.concatenate_forms(existing_farm.forms, new_farm.forms)

        # Merge warnings
        for warning_category, warnings in new_farm.warnings.items():
            existing_farm.warnings[warning_category].extend(warnings)

        return existing_farm

    def _concatenate_forms(self, existing_forms: dict[str, Form], new_forms: dict[str, Form]) -> dict[str, Form]:
        for key in new_forms.keys():
            if not new_forms[key]:
                continue

            if not existing_forms[key]:
                existing_forms[key] = new_forms[key]
                continue

            current_last_image = existing_forms[key][0].images[-1]
            new_image = new_forms[key][0].images[0]
            if len(new_forms[key][0].images) == 1 and (new_image.number == current_last_image.number + 1):
                existing_forms[key][0].images.append(new_image)
                self.concatenate_instance_attributes(existing_forms[key][0], new_forms[key][0], 'field_info_date')
                self.concatenate_instance_attributes(existing_forms[key][0], new_forms[key][0], 'primary_record_date')

            else:
                existing_forms[key].append(new_forms[key][0])

        return existing_forms

    def assign_ids_to_filenames(self):
        """_summary_

        Args:
            csv_data (dict): _description_
        """
        
        for list_of_transcriptions in self.source_data.values():
            for transcription in list_of_transcriptions:
                self.files.update({transcription.file1.name: create_uuid_str()})
                if transcription.file2:
                    self.files.update({transcription.file2.name: create_uuid_str()})

