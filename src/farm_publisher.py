"""
farm_Publisher

This module runs the second stage of the ETL pipeline for the Farm Survey data analysis work. 
The stage starts with the proof file for a single county initially returned by MAF32_Harvester after it has been reviewed, and possibly edited, by the CTD team. 
The proof data is transformed into JSON documents in the Discovery schema
The image size information required to complete the JSON documents is not available to to this application, so the JOSN documents partially complete.
The documents are manually sent to the Digital Archiving team, who will add the image sizes and the drop the final JSONs in an S3 bucket for ingest by Discovery

The ETL stages in this module are:
Extract:
* extract and clean the farm proof data
Transform:
* convert each proof Excel row into a DiscoveryMAF32 dataclass instance
Load
* output each farm as a Discovery JSON document (without the image size values)

Yields:
    a set of JSON documents in the Pipeline/#3-PUBLISH folder
"""
import json
import pprint
import shelve

from _dataclasses.farm_record import DiscoveryMAF32
from src._tools.constants import PATH
from src._tools.helpers import clean_excel_data, load_excel_data
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def build_catalogue_documents(cleaned_data: list[dict], farms_store: dict, test_mode=False) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for farm_proof in cleaned_data:
        discovery_document = DiscoveryMAF32(farm_proof)
        logger.info(f"Farm {farm_proof['catalogue_reference']} --> Built record {farm_proof['farm_id']} with {len(discovery_document.files)} images")

        documents.append(discovery_document.to_dict())

    return documents


def write_catalogue_documents(documents: list[dict], county: str) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    publish_dir = PATH.PUBLISH / f"{county}/MAF 32/"
    publish_dir.mkdir(exist_ok=True, parents=True)
    for document in documents:
        with open(publish_dir / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"Record for farm {document['record']['citableReference']}: {final_file.name} DONE")
            json.dump(document, final_file)   
           
            
def process_proof_files(test_mode: bool=False) -> None:
    xlsx_files = PATH.HARVEST.glob("TEST/*.xlsx") if test_mode else PATH.HARVEST.glob("*.xlsx")

    for proof_file in xlsx_files:
        county, _ = proof_file.name.split("_", maxsplit=1)
        with shelve.open(PATH.FARMS_DB, "r") as farms_db:
            farms_store = farms_db[county]
        proof_data = load_excel_data(proof_file)
        cleaned_data = clean_excel_data(proof_data)
        final_documents = build_catalogue_documents(cleaned_data, farms_store, test_mode)
        if test_mode:
            for document in final_documents:
                pretty.pprint(document)
        write_catalogue_documents(final_documents, county)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    process_proof_files()


if __name__ == "__main__":
    main(test_mode=False)

