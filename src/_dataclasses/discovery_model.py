"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field
from urllib import parse
import requests
import re
import uuid
import dbm

from src._tools.constants import DISCOVERY, PATH
from src._tools.helpers import create_uuid_str
    

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
        parent_record = result.json()

        return parent_record['records'][0]['id']

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

