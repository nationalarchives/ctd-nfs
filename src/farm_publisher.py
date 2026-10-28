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
import tomllib
from collections.abc import Generator
from itertools import batched
from pathlib import Path
from shutil import make_archive, rmtree
from time import sleep

from src._dataclasses.farm_combine import FarmForDiscovery, HarvestedFarm
from src._dataclasses.farm_record import DiscoveryMAF32
from src._tools.constants import PATH, REGEX
from src._tools.logging_setup import create_logger
from src.farm_harvester import read_farms_db

logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def build_catalogue_documents(harvested_farms: Generator[HarvestedFarm], update_scope: str) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for batch in batched(harvested_farms, 1000):
        for farm in batch:
            farm_for_discovery = FarmForDiscovery(farm)
            discovery_document = DiscoveryMAF32(farm_for_discovery, update_scope)
            logger.info(f"Farm {farm.farm_reference} --> Built record {farm_for_discovery.id} with {len(discovery_document.files)} images")

            documents.append(discovery_document.to_dict())
        
        logger.info(" zzzzzzzzzzz 15 SECOND BATCH PAUSE zzzzzzzzzzz")
        sleep(15)

    return documents


def write_jsons_to_zip_archive(county: str, version: str):
    logger.info(" ===== CREATING ZIP ARCHIVE ===== ")
    
    directory = PATH.PUBLISH / f"{county}/"
    archive_name = f"{directory}_MAF32"
    make_archive(
        archive_name,
        'zip',
        root_dir=PATH.PUBLISH,
        base_dir=f"{county}/MAF32/{version}",
    )


def write_catalogue_documents(documents: list[dict], county: str, version: str) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    publish_dir = PATH.PUBLISH / f"{county}/MAF32/{version}/"

    if publish_dir.exists():
        rmtree(publish_dir)
    publish_dir.mkdir(parents=True)
    for document in documents:
        with open(publish_dir / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"Record for farm {document['record']['citableReference']}: {final_file.name} DONE")
            json.dump(document, final_file)   
           
            
def process_proof_files(config: dict) -> None:
    input_files = PATH.INPUT.glob("TEST/*MAF32_HarvesterIN_*.csv") if config['test_mode'] else PATH.INPUT.glob("*MAF32_HarvesterIN_*.csv")

    for csv_file in input_files:
        county, _ = csv_file.name.split(" ", maxsplit=1)
        version = REGEX.TRANSCRIPTIONS_VERSION.match(csv_file.stem)['version']

        county_data = read_farms_db(county, config['test_mode'])
        harvested_farms = iter(county_data[version].values())

        final_documents = build_catalogue_documents(harvested_farms, config['update_scope'])
        write_catalogue_documents(final_documents, county, version)
        write_jsons_to_zip_archive(county, version)
        logger.info("--- pausing for two minutes before next file ---")
        sleep(120)


def main():
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    with open(Path(r"src/run_options.toml"), mode="rb") as fp:
        config = tomllib.load(fp)

    process_proof_files(config['farm_publisher'])


if __name__ == "__main__":
    main()

