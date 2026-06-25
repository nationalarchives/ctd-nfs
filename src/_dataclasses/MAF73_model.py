import requests
import re
import uuid
from dataclasses import dataclass
from urllib import parse
import dbm

from src._tools.helpers import create_uuid_str
from src._tools.constants import DISCOVERY, PATH


@dataclass
class ImageFile:
    name: str

    @property
    def id(self) -> uuid.UUID:
        with dbm.open(PATH.FILE_IDS, 'c') as file_ids_db:
            db_id = file_ids_db.get(self.name, "")
            if db_id:
                id = db_id.decode()
            else:
                id = create_uuid_str()
                file_ids_db[self.name] = id
        return id


def get_map_ids(reference: str) -> dict[str, uuid.UUID]:
    with dbm.open(PATH.FARM_IDS, 'c') as farm_ids_db:
        db_ids = farm_ids_db.get(reference, "")
        if db_ids:
            db_ids = eval(db_ids.decode())
            map_ids = {
                'id': db_ids['id'],
                'replica_id': db_ids['replica_id'],
            }
        else:
            _ids = "{'id': '%s', 'replica_id': '%s'}" % (create_uuid_str(), create_uuid_str())
            farm_ids_db[reference] = _ids
            map_ids = eval(_ids)

    return map_ids


@dataclass
class DiscoveryMAF73:
    map_data: dict
    # update_scope: str = DISCOVERY.UPDATE_SCOPE['update_metadata_not_digital_files']
    update_scope: str = DISCOVERY.UPDATE_SCOPE['new_record_with_digital_files']

    def __post_init__(self):
        self._map_ids = get_map_ids(self.map_data['Reference'])
        self.id: uuid.UUID = self._map_ids['id']
        self.replica_id: uuid.UUID = self._map_ids['replica_id']

    @property
    def parent_id (self) -> str:
        ref = self.map_data['Reference'].rsplit("/", maxsplit=1)[0]
        ref_url_safe = parse.quote(ref)

        api_query = fr"{DISCOVERY.API_URI}/search/records?sps.searchQuery={ref_url_safe}"
        result = requests.get(api_query)

        for record in result.json()['records']:
            if record['reference'] == ref:
                return record['id']

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
        _, reference_part = self.map_data['Reference'].rsplit("/", maxsplit=1)
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
                'referencePart': reference_part,
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
    
