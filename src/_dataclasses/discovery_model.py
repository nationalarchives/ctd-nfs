"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field, InitVar
import requests
from urllib import parse

from src._dataclasses.farm_model import Farm
from src._tools.constants import DISCOVERY
from src._tools.helpers import create_uuid_str
        

@dataclass
class Image:
    original_name: str
    id: InitVar[str] = ""
    
    def __post_init__(self, id):
        self.name = f"66/MAF/32/{id}.jpg"


@dataclass
class Replica:
    id: str = field(default_factory=create_uuid_str)
    files: list[Image]
    

@dataclass
class Discovery:
    farm: Farm
    replica_id: Replica
    update_scope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']

    def _get_parent_id(self) -> str:
        ref = self.farm.catalague_reference.rsplit("/", maxsplit=1)[0]
        ref_url_safe = parse.quote(ref)

        api_query = fr"{DISCOVERY.API_URI}/search/records?sps.searchQuery={ref_url_safe}"
        result = requests.get(api_query)
        parent_record = result.json()

        return parent_record['records'][0]['id']

    def __post_init__(self):
        self.parent_id = self._get_parent_id()

    @property
    def scope_and_content(self) -> dict:
        description_fields = {
            'Farm Reference': self.farm.farm_reference,
            'Farm Name': self.farm.farm_name,
            'addressee':'Addressee(s)',
            'Farmer(s) or occupier(s)': self.farm.farmer,
            'Landowner(s)': self.farm.landowner,
            'Acreage': self.farm.acreage,
            'OS Sheet Number': self.farm.os_sheet_number,
            'Field Info Date': self.farm.field_info_date,
            'Primary Record Date': self.farm.primary_record_date,
            'Record consists of': self.farm.forms,
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

    def to_dict(self) -> dict:
        { 
            'record': {
                'iaid': self.farm.iaid,
                'citableReference': self.farm.catalogue_reference,
                'replicaId': self.replica.id,
                'parentId': self.parent_id,
                'scopeContent': self.scope_and_content,
            } | DISCOVERY.RECORD_CONSTANTS,
            'updateScope': self.update_scope,
            'replica': {
                'files': [
                    {
                    'originalName': image.original_name,
                    'format': "jpg",
                    'name': image.name,
                    }
                    for image in self.replica.files
                ],
                'replicaId': self.replica.id,
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }

