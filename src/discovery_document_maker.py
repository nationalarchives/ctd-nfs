from _config.constants import PATH

import json


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


if __name__ == "__main__":
    create_discovery_final_documents()


