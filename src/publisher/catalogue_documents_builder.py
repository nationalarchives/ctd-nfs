from dataclasses import asdict

from src._tools.constants import PATH, DATA, DISCOVERY
from src.harvester.farm_setup import Farm
from src.publisher.record_setup import Image, Record, Replica


def create_description(row_data: dict) -> str:
    description_values = {
        key: row_data[key]
        for key in DISCOVERY.DESCRIPTION_FIELDS
    }

    return DISCOVERY.DESCRIPTION_TEMPLATE.substitute(description_values)


def build_record_subdocument(farm_iaid: str, row: dict) -> Record:
    record = Record(
            iaid=farm_iaid,
            citableReference=row['catalogue_reference'],
        )
    record.scopeContent['description'] = create_description(row)

    return record


def build_replica_subdocument(filenames: str, iaid: str, replica_id: str) -> Replica:
    files_data = [
        Image(originalName=filename.strip(",;"))
        for filename in filenames.split()
    ]

    return Replica(
        replicaId=replica_id,
        files=files_data
    )


def build_catalogue_documents(cleaned_data: list[dict]) -> list[dict]:
    documents = []
    for row in cleaned_data:
        record = build_record_subdocument(row)
        replica = build_replica_subdocument(row['Filenames'], record.iaid, record.replicaId)
        documents.append({'record': asdict(record), 'replica': asdict(replica)})

    return documents

