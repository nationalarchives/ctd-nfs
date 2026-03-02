from urllib import parse
import json

import requests

from _config.constants import DATA, PATH
from discovery_data_processor import output_json_files
from record_builder import Image, Record, Replica


def create_discovery_final_documents() -> None:
    for record_file in PATH.TEST_OUTPUT.glob("parts/*_record.json"):
        iaid = str(record_file.stem).split("_")[0]
        replica_file = PATH.TEST_OUTPUT / f"parts/{iaid}_replica.json"

        with open(record_file, 'r') as rec_file, \
            open(replica_file, 'r') as rep_file, \
            open(PATH.TEST_OUTPUT / f"{iaid}.json", 'w') as final_file:

            record_document = json.load(rec_file)
            replica_document = json.load(rep_file)

            output_record = {'record': record_document, 'replica': replica_document}
            json.dump(output_record, final_file)


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
    image_data = [
        Image(file_name=filename.strip(",;"), sequence_no=index)
        for index, filename in enumerate(filenames.split(), start=1)
    ]

    return Replica(
        iaid,
        replica_id,
        images=image_data
    )


def build_catalogue_documents(cleaned_data: list[dict]) -> list[dict]:
    documents = []
    for row in cleaned_data:
        record = build_record_subdocument(row)
        replica = build_replica_subdocument(row['Filenames'], record.iaid, record.replicaId)
        documents.append({'record': asdict(record), 'replica': asdict(replica)})

    return documents


if __name__ == "__main__":
    create_discovery_final_documents()
