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
    citableReference: str # catalogue reference e.g. "MAF 32/348/56/12"
    replicaId: str = field(default_factory=create_uuid_str)
    scopeContent: dict = field(default_factory=scope_and_content)

    def __post_init__(self):
        self.parentId = _get_parent_id(self.citableReference)

    def to_dict(self) -> dict:       
        return {
            'iaid': self.iaid,
            'citableReference': self.citableReference,
            'replicaId': self.replicaId,
            'parentId': self.parentId,
            'scopeContent': self.scopeContent,
        } | DISCOVERY.RECORD_CONSTANTS
        

@dataclass
class Image:
    originalName: str
    id: InitVar[str] = ""
    
    def __post_init__(self, id):
        self.name = f"66/MAF/32/{id}.jpg"


@dataclass
class Replica:
    replicaId: str # must be same as replicaId in record instance
    files: list[Image]

    def to_dict(self) -> dict:
        images = [
            {
            'originalName': image.originalName,
            'format': "jpg",
            'name': image.name,
            }
            for image in self.files
        ]
        
        return {
        'files': images,
        'replicaId': self.replicaId,
        'origination': "DigitalSurrogate",
        'totalSize': None,
        }
    

@dataclass
class Discovery:
    record: Record
    replica: Replica
    updateScope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']
    
    def to_dict(self) -> dict:
        { 
            'record': {
                'iaid': self.record.iaid,
                'citableReference': self.record.citableReference,
                'replicaId': self.record.replicaId,
                'parentId': self.record.parentId,
                'scopeContent': self.record.scopeContent,
            } | DISCOVERY.RECORD_CONSTANTS,
            'updateScope': self.updateScope,
            'replica': {
                'files': [
                    {
                    'originalName': image.originalName,
                    'format': "jpg",
                    'name': image.name,
                    }
                    for image in self.replica.files
                ],
                'replicaId': self.replica.replicaId,
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }
