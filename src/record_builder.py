"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field
import uuid


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

def create_uuid_str():
    return str(uuid.uuid4())

@dataclass
class Record:
    """ must be provided at instantiation """
    citableReference: str # catalogue reference e.g. "MAF 32/348/56/12"
    parentId: str # str(uuid) e.g. "8b2a43dd-752d-44a7-8163-2b64bb6e6cd0"

    """ generated at instantiation """
    iaid: str = field(default_factory=create_uuid_str)
    replicaId: str = field(default_factory=create_uuid_str)

    """ constants """
    catalogueLevel: int =  8
    coveringFromDate: int = 19410101
    coveringToDate: int = 19431231
    chargeType: int =  1
    coveringDates: str =  "1941-1943"
    closureStatus: str =  "Open Document, Open Description"
    digitised: bool =  True
    heldBy: list = field(default_factory=held_by)
    legalStatus: str = "Public Record(s)"
    referencePart: str = "0"
    scopeContent: dict = field(default_factory=description)
    source: str =  "FS"
    title: str = "title"

@dataclass
class Replica:
    IAID: str
    replicaId: str
    images: list


