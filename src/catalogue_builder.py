from urllib import parse
from dataclasses import asdict

import requests

from _config.constants import DATA
from record_builder import Image, Record, Replica


def get_parent_id(raw_reference: str) -> str:
    ref = raw_reference.rsplit("/", maxsplit=1)[0]
    ref_url_safe = parse.quote(ref)

    api_query = fr"{DATA.DISCOVERY_API_URI}/search/records?sps.searchQuery={ref_url_safe}"
    result = requests.get(api_query)

    parent_record = result.json()

    return parent_record['records'][0]['id']


def create_description(row_data: dict) -> str:
    scope_and_content = [
    f"{key}: {row_data[key]}<p>"
    for key in DATA.DESCRIPTION_FIELDS
    ]

    return "".join(scope_and_content)


def build_record_subdocument(row: dict) -> Record:
    parent_id = get_parent_id(row['Reference'])
    description = create_description(row)
    return Record(
            citableReference=row['Reference'],
            parentId=parent_id,
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

