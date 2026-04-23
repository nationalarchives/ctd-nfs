"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field, InitVar
import requests
from urllib import parse

from src._dataclasses.farm_model import Farm
from src._tools.constants import DISCOVERY
from src._tools.helpers import create_uuid_str


def scope_and_content():
    return {
        'description': "",
        }
        

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
    replica: Replica
    scope_and_content: dict = field(default_factory=scope_and_content)
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

