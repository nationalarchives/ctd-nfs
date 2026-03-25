from dataclasses import asdict

from src._config.constants import DATA
from src.publisher.record_setup import Image, Record, Replica


def create_description(row_data: dict) -> str:
    scope_and_content = [
    f"{key}: {row_data[key]}<p>"
    for key in DATA.DESCRIPTION_FIELDS
    ]

    return "".join(scope_and_content)


def build_record_subdocument(row: dict) -> Record:
    description = create_description(row)
    return Record(
            citableReference=row['Reference'],
            scopeContent={'description': description},
            title=row['Farm Number'],
        )


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

