"""
"""
import os
import json
from dataclasses import asdict

from discovery_document_maker import create_discovery_sub_documents
from src._config.constants import PATH
from src._tools.xlreader import read_file
from src.record_builder import Record, Replica


def load_excel_data() -> list[dict]:
    data_file = PATH.TEST_INPUT / "Rutland - Interim to Final.xlsx"
    excel_data = read_file(data_file)

    column_names = excel_data['Sheet'][0]

    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data["Sheet"][1:]
        if row_data[0]
    ]


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
    discovery_data = []
    non_breaking_space = "\xa0"
    for row in raw_csv_data:
        cleaned_data_row = {}
        for key, value in row.items():
            if not value or type(value) is not str:
                cleaned_data_row[key] = value
                continue

            value = value.strip()
            value = value.replace(f"{non_breaking_space}", " ")
            value = value.replace("\n", "")
            cleaned_data_row[key] = value

        discovery_data.append(cleaned_data_row)
    
    return discovery_data




def output_json_files(record: Record, replica: Replica) -> None:
    os.makedirs(PATH.TEST_OUTPUT, exist_ok=True)

    record_file = PATH.TEST_OUTPUT / f"parts/{record.iaid}_record.json"
    replica_file = PATH.TEST_OUTPUT / f"parts/replica_manifests/{record.iaid}_replica_manifest.json"

    with open(record_file, 'w') as file_rec, open(replica_file, 'w') as file_rep:
        print(f"{record_file.name=}, {replica_file.name=}")
        json.dump(asdict(record), file_rec, indent=4)
        json.dump(asdict(replica), file_rep, indent=4)
            
            
def create_discovery_sub_documents() -> None:
    excel_data = load_excel_data()
    cleaned_data = clean_excel_data(excel_data)

    for row in cleaned_data:
        parent_id = get_parent_id(row['Reference'])
        description = create_description(row)
        record = Record(
            citableReference=row['Reference'],
            parentId=parent_id,
            scopeContent={'description': description},
            title=row['Farm Number'],
        )

        replica = create_replica_set(row['Filenames'], record.iaid, record.replicaId)

        output_json_files(record, replica)


if __name__ == "__main__":
    create_discovery_sub_documents()

