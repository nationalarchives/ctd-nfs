import re
import uuid
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal
from urllib import parse

from src._tools.constants import DISCOVERY, REGEX
from src._tools.helpers import create_uuid_str, get_parent_discovery_record


@dataclass
class ImageFile:
    name: str
    id: uuid.UUID = field(default_factory=create_uuid_str)


type Scope = Literal['RecordAndReplica', 'RecordOnly']

@dataclass
class DiscoveryMAF73:
    map_data: dict
    update_scope: Scope = "RecordAndReplica"

    def __post_init__(self):
        self.id: uuid.UUID = self.map_data['id']
        self.replica_id: uuid.UUID = self.map_data['replica_id']
        _reference = REGEX.REFERENCE.match(self.map_data['Reference'])
        self.reference_stem = _reference['stem']
        self.reference_part = _reference['part']

    @cached_property
    def parent_id (self) -> str:
        ref_url_safe = parse.quote(self.reference_stem, safe="")

        parent_record = get_parent_discovery_record(ref_url_safe)

        return parent_record['assets'][0]['id']

    @property
    def scope_and_content(self) -> dict:
        description = [
            f"<p>{field_name}: {self.map_data[field_name]}"
            for field_name in ['Map Sheet Number', 'Map Edition', 'Miscellaneous Comments', 'Parish(es)', 'Annotation Date(s)',]
            if self.map_data[field_name]
        ]

        return {
            'description': "".join(description),
        }

    @property
    def files(self) -> list:
        images = [
            ImageFile(name)
            for name in re.split(r"[;,] *", self.map_data['Filenames'])
        ]
        return [
            {
                'originalName': img.name,
                'format': "jpg",
                'name': f"66/MAF/73/{img.id}.jpg",
            }
            for img in images
        ]

    def to_dict(self) -> dict:
        possible_optional = {
            'note': self.map_data['Note'],
            'formerReferenceDep': str(self.map_data['Former reference in its original department']),
            'mapScaleNumber': int(self.map_data['Map scale']) if self.map_data['Map scale'] else None,
            'physicalCondition': self.map_data['Physical condition'],
        }
        actual_optional = {
            key: value
            for key, value in possible_optional.items()
            if value
        }

        return {
            'record': {
                'iaid': self.id,
                'citableReference': self.map_data['Reference'],
                'replicaId': self.replica_id,
                'parentId': self.parent_id,
                'scopeContent': self.scope_and_content,
                'referencePart': self.reference_part,
                'catalogueLevel': 7,
                'accessConditions': "Closed for 50 years",
            } | actual_optional | DISCOVERY.MAF73_RECORD_CONSTANTS,
            'updateScope': self.update_scope,
            'replica': {
                'files': self.files,
                'replicaId': self.replica_id,
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }

    def for_index(self) -> dict:
        possible_note = {'note': self.map_data['Note']} if self.map_data['Note'] else {}
        return {
            'record': {
                'iaid': self.id,
                'citableReference': self.map_data['Reference'],
                'replicaId': self.replica_id,
                'parentId': self.parent_id,
                'scopeContent': {'description': self.map_data['Miscellaneous Comments']},
                'referencePart': self.reference_part,
                'catalogueLevel': 7,
                'accessConditions': "Closed for 50 years",
            } | possible_note | DISCOVERY.MAF73_RECORD_CONSTANTS,
            'updateScope': self.update_scope,
            'replica': {
                'files': self.files,
                'replicaId': self.replica_id,
                'origination': "DigitalSurrogate",
                'totalSize': None,
            }
        }

    
