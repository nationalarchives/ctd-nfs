"""
"""
import json
import pprint

from src._tools.constants import PATH
from src._tools.xlreader import read_file
from src._tools.logging_setup import create_logger
from src.publisher.catalogue_documents_builder import build_catalogue_documents


logger = create_logger("src._config", "logging.yaml")
pretty = pprint.PrettyPrinter(indent=4)


def load_excel_data() -> list[dict]:
    # TODO: read file from INPUT folder without hardcoding and parse county from filename
    data_file = PATH.INPUT / "RD Rutland Final Proof.xlsx"
    logger.info(F" ===== LOADING PROOF FILE {data_file.name}===== ")
    excel_data = read_file(data_file)

    column_names = excel_data['Proof data'][0]

    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data["Proof data"][1:]
        if row_data[0]
    ]


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
    logger.info(" ===== CLEANING PROOF DATA ===== ")
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


def write_catalogue_documents(documents: list[dict]) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    for document in documents:
        with open(PATH.PUBLISH / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"{final_file.name}")
            json.dump(document, final_file)   
           
            
def main(test_mode=False):
    excel_data = load_excel_data()
    cleaned_data = clean_excel_data(excel_data)
    final_documents = build_catalogue_documents(cleaned_data, test_mode)
    if test_mode:
        for document in final_documents:
            pretty.pprint(document)
    write_catalogue_documents(final_documents)


if __name__ == "__main__":
    main(test_mode=True)