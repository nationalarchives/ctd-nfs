"""
Dataclasses and factories used to create Discovery JSON records
"""
from dataclasses import dataclass


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
    heldBy: list
    legalStatus: str
    referencePart: str
    scopeContent: dict
    source: str
    title: str

