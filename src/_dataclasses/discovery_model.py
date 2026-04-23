"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field
from urllib import parse
import requests

from src._dataclasses.farm_model import Farm
from src._tools.constants import DISCOVERY
from src._tools.helpers import create_uuid_str
    

@dataclass
class Discovery:
    farm: Farm
    replica_id: str = field(default_factory=create_uuid_str)
    update_scope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']

    @property
    def parent_id (self) -> str:
        ref = self.farm.catalogue_reference.rsplit("/", maxsplit=1)[0]
        ref_url_safe = parse.quote(ref)

        api_query = fr"{DISCOVERY.API_URI}/search/records?sps.searchQuery={ref_url_safe}"
        result = requests.get(api_query)
        parent_record = result.json()

        return parent_record['records'][0]['id']

    @property
    def forms_list(self) -> str:
        forms_ouptut = []
        for form_type, transcriptions in self.source_data.items():
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
            'Farm Reference': self.farm.farm_reference,
            'Farm Name': self.farm.farm_name,
            'addressee': self.farm.addressee,
            'Farmer(s) or occupier(s)': self.farm.farmer,
            'Landowner(s)': self.farm.landowner,
            'Acreage': self.farm.acreage,
            'OS Sheet Number': self.farm.os_sheet_number,
            'Field Info Date': self.farm.field_info_date,
            'Primary Record Date': self.farm.primary_record_date,
            'Record consists of': self.forms_list,
        }
        if self.farm.additional_farms:
            description_fields['Forms present on other Records'] = self.farm.additional_farms

        description = [
            f"{key}: {value}<p>"
            for key, value in description_fields.items()
        ]

        return {
            'description': "".join(description),
        }
    
    @property
    def files(self) -> list:
        return [
            {
                'originalName': image.name,
                'format': "jpg",
                'name': f"66/MAF/32/{image.id}.jpg",
            }
            for each_form in self.farm.forms
            for image in each_form.images
        ]

    def to_dict(self) -> dict:
        { 
            'record': {
                'iaid': self.farm.iaid,
                'citableReference': self.farm.catalogue_reference,
                'replicaId': self.replica_id,
                'parentId': self.parent_id,
                'scopeContent': self.scope_and_content,
            } | DISCOVERY.RECORD_CONSTANTS,
            'updateScope': self.update_scope,
            'replica': {
                'files': self.files,
                'replicaId': self.replica_id,
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }

