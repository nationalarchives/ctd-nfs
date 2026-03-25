"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field
import uuid
import shelve
import requests
from urllib import parse

from src._config.constants import DATA
from src._config.constants import PATH
from src._tools.helpers import create_uuid_str


def description():
    return {'description': ""}

def held_by():
    """ constant for Record.heldBy attribute """
    return [
        {
            "xReferenceId": "A13530124",
            "xReferenceCode": "66",
            "xReferenceName": "The National Archives, Kew",
        }
    ]

def _create_uuid_filename():
    return f"66/MAF/32/{uuid.uuid4()}.jpg"

def _get_farm_iaid(catalogue_reference: str) -> str:
    with shelve.open(PATH.FARMS_DB, "r") as farms_db:   
        farms = (
            reference['Farm']
            for county in farms_db
            for reference in farms_db[county]
            if reference == catalogue_reference
        )
    farm_instance = next(farms, None)
    
    return farm_instance.iaid

def _get_parent_id(catalague_reference: str) -> str:
    ref = catalague_reference.rsplit("/", maxsplit=1)[0]
    ref_url_safe = parse.quote(ref)

    api_query = fr"{DATA.DISCOVERY_API_URI}/search/records?sps.searchQuery={ref_url_safe}"
    result = requests.get(api_query)
    parent_record = result.json()

    return parent_record['records'][0]['id']

closure_status = {
	'Closed Or Retained Document, Closed Description': "C",
	'Closed Or Retained Document, Open Description': "D",
	'Open Document, Open Description': "O",
	'Partially Closed… not currently used': "P",
}

@dataclass
class Record:
    """ must be provided at instantiation """
    citableReference: str # catalogue reference e.g. "MAF 32/348/56/12"

    """ generated at instantiation """
    replicaId: str = field(default_factory=create_uuid_str)

    """ constants """
    catalogueLevel: int =  8
    coveringFromDate: int = 19410101
    coveringToDate: int = 19431231
    chargeType: int =  1
    coveringDates: str =  "1941-1943"
    closureStatus: str =  closure_status['Open Document, Open Description']
    digitised: bool =  True
    heldBy: list = field(default_factory=held_by)
    legalStatus: str = "Public Record(s)"
    referencePart: str = "0"
    scopeContent: dict = field(default_factory=description)
    source: str =  "FS"
    title: str = "title"

    def __post_init__(self):
        self.iaid = _get_farm_iaid(self.citableReference)
        self.parentId = _get_parent_id(self.citableReference)
        

@dataclass
class Image:
    originalName: str
    format: str = "jpg"
    name: str = field(default_factory=_create_uuid_filename)

@dataclass
class Replica:
    replicaId: str
    files: list[Image]
    origination: str = "DigitalSurrogate"
    totalSize: None


