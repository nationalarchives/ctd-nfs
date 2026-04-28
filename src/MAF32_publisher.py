"""
"""
import json
import pprint
import shelve

from src._tools.constants import PATH
from src._tools.xlreader import read_file
from src._tools.logging_setup import create_logger
from src._dataclasses.discovery_model import DiscoveryMAF32
from src._dataclasses.farm_model import Details, Farm


logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def load_excel_data() -> list[dict]:
    # TODO: read file from INPUT folder without hardcoding and parse county from filename
    data_file = PATH.HARVEST / "RD Rutland final for JSON.xlsx"
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


def build_catalogue_documents(cleaned_data: list[dict], farms_store: dict, test_mode=False) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for row in cleaned_data:
        farm = farms_store[row['catalogue_reference']]
        farm.farm_name = row['farm_name']
        farm.landowner = Details(full_address=row['landowner'])
        farm.farmer = Details(full_address=row['farmer'])
        farm.addressee = Details(full_address=row['addressee'])
        farm.acreage = row['acreage']
        farm.OS_map_sheet = row['os_sheet_number']
        farm.field_info_date = row['field_info_date']
        farm.primary_record_date = row['primary_record_date']
        # TODO: write farm back to farm_store and return farm_store to update shelf

        discovery_document = DiscoveryMAF32(farm)
        logger.info(f"Farm {farm.catalogue_reference} --> Built record {farm.iaid} with {len(discovery_document.files)} images")

        documents.append(discovery_document.to_dict())

    return documents


def write_catalogue_documents(documents: list[dict]) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    for document in documents:
        with open(PATH.PUBLISH / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"Record for farm {document['record']['citableReference']}: {final_file.name} DONE")
            json.dump(document, final_file)   
           
            
def process_proof_files(test_mode: bool=False) -> None:
    proof_files = PATH.TEST_PUBLISH.glob("*.xlsx") if test_mode else PATH.PUBLISH.glob("*.xlsx")


    for excel_file in proof_files:
        county, _ = excel_file.name.split("_")
        with shelve.open(PATH.FARMS_DB, "r") as farms_db:
            farms_store = farms_db[county]
        proof_data = load_excel_data(excel_file)
        cleaned_data = clean_excel_data(proof_data)
        final_documents = build_catalogue_documents(cleaned_data, farms_store, test_mode)
        if test_mode:
            for document in final_documents:
                pretty.pprint(document)
        write_catalogue_documents(final_documents)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    process_proof_files()


if __name__ == "__main__":
    main(test_mode=False)