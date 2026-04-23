"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field, InitVar
import requests
from urllib import parse

from src._tools.constants import DISCOVERY
from src._tools.helpers import create_uuid_str


def scope_and_content():
    return {
        'description': "",
        }


def _get_parent_id(catalague_reference: str) -> str:
    ref = catalague_reference.rsplit("/", maxsplit=1)[0]
    ref_url_safe = parse.quote(ref)

    api_query = fr"{DISCOVERY.API_URI}/search/records?sps.searchQuery={ref_url_safe}"
    result = requests.get(api_query)
    parent_record = result.json()

    return parent_record['records'][0]['id']


@dataclass
class Record:    
    iaid: str # must be same as iaid from farm instance
    citable_reference: str # catalogue reference e.g. "MAF 32/348/56/12"
    scope_and_content: dict = field(default_factory=scope_and_content)

    def __post_init__(self):
        self.parent_id = _get_parent_id(self.citable_reference)
        

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
    record: Record
    replica: Replica
    update_scope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']
    
    def to_dict(self) -> dict:
        { 
            'record': {
                'iaid': self.record.iaid,
                'citableReference': self.record.citable_reference,
                'replicaId': self.replica.id,
                'parentId': self.record.parent_id,
                'scopeContent': self.record.scope_and_content,
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
