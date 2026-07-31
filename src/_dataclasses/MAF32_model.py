"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass
from urllib import parse
import requests
import re

from src._tools.constants import DISCOVERY
    

@dataclass
class DiscoveryMAF32:
    farm: dict
    update_scope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']

    @property
    def parent_id (self) -> str:
        ref = self.farm['catalogue_reference'].rsplit("/", maxsplit=1)[0]
        ref_url_safe = parse.quote(ref)

        api_query = fr"{DISCOVERY.API_URI}/search/records?sps.searchQuery={ref_url_safe}"
        result = requests.get(api_query)
        parent_record = result.json()

        return parent_record['records'][0]['id']

    @property
    def forms_list(self) -> str:
        forms_ouptut = []
        for form_type, transcriptions in self.farm.source_data.items():
            if not transcriptions:
                continue

            if len(transcriptions) == 1:
                forms_ouptut.append(form_type)
            else:
                for index in range(len(transcriptions)):
                    forms_ouptut.append(f"{form_type} [{index + 1}]")

        return "; ".join(forms_ouptut)


    @property
    def scope_and_content(self) -> dict:
        description_fields = {
            'Farm Reference': f"{self.farm['farm_number']}.",
            'Farm Name(s)': f"{self.farm['farm_name']}.",
            'Addressee(s)': f"{self.farm['addressee']}.",
            'Farmer(s) or Occupier(s)': f"{self.farm['farmer']}.",
            'Landowner(s)': f"{self.farm['landowner']}.",
            'Acreage(s)': f"{self.farm['acreage']}.",
            'OS Sheet Number(s)': f"{self.farm['os_sheet_number']}.",
            'Field Information Date(s)': f"{self.farm['field_info_date']}.",
            'Primary Record Date(s)': f"{self.farm['primary_record_date']}.",
            'Record consists of': f"{self.farm['forms']}.",
        }

        description = [
            f"<p>{key}: {value}"
            for key, value in description_fields.items()
        ]

        return {
            'description': "".join(description),
        }
    
    @property
    def files(self) -> list:
        return [
            {
                'originalName': name,
                'format': "jpg",
                'name': f"66/MAF/32/{id}.jpg",
            }
            for (id, name) in zip(re.split(r"[;,] *", self.farm['file_ids']), re.split(r"[;,] *", self.farm['file_names']))
        ]

    def to_dict(self) -> dict:
        _, reference_part = self.farm['catalogue_reference'].rsplit("/", maxsplit=1)
        return { 
            'record': {
                'iaid': self.farm['farm_id'],
                'citableReference': self.farm['catalogue_reference'],
                'replicaId': self.farm['replica_id'],
                'parentId': self.parent_id,
                'scopeContent': self.scope_and_content,
                'referencePart': reference_part,
            } | DISCOVERY.MAF32_RECORD_CONSTANTS,
            'updateScope': self.update_scope,
            'replica': {
                'files': self.files,
                'replicaId': self.farm['replica_id'],
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }


