"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field
import uuid
import shelve
import requests

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
    parentId: str # str(uuid) e.g. "8b2a43dd-752d-44a7-8163-2b64bb6e6cd0"

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


