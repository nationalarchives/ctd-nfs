"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass, field


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

@dataclass
class Record:
    citableReference: str
    parentId: str
    iaid: str
    replicaId: str
    catalogueLevel: int
    coveringFromDate: int
    coveringToDate: int
    chargeType: int
    coveringDates: str
    closureStatus: str
    digitised: bool
    heldBy: list = field(default_factory=held_by)
    legalStatus: str
    referencePart: str
    scopeContent: dict = field(default_factory=description)
    source: str
    title: str

