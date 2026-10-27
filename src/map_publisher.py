import json
import pprint
import tomllib
from itertools import batched
from pathlib import Path
from shutil import make_archive, rmtree
from time import sleep

from src._dataclasses.map_record import DiscoveryMAF73
from src._tools.constants import PATH
from src._tools.helpers import clean_excel_data, create_uuid_str, load_excel_data
from src._tools.logging_setup import create_logger
from src.farm_harvester import read_farms_db

logger = create_logger("src._config", "logging.yaml")
pretty = pprint.PrettyPrinter(indent=4)


def build_catalogue_documents(map_data: list[dict], update_scope) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for batch in batched(map_data, 1000):
        for map_proof in batch:
            map_document = DiscoveryMAF73(map_proof, update_scope)

            logger.info(f"Farm {map_proof['Reference']} --> Built record {map_document.id} with {len(map_document.files)} images")

            documents.append(map_document.to_dict())
        logger.info(" zzzzzzzzzzz 15 SECOND BATCH PAUSE zzzzzzzzzzz")
        sleep(15)
 
    return documents


def add_ids_to_maps(map_data: list[dict], existing_maps: dict) -> list[dict]:
    amended_map_data: list[dict] = []

    for map in map_data:
        if map['Reference'] in existing_maps:
            map['id'] = existing_maps[map['Reference']]['id']
            map['replica_id'] = existing_maps[map['Reference']]['replica_id']
        else:
            map['id'] = create_uuid_str()
            map['replica_id'] = create_uuid_str()

        amended_map_data.append(map)

    return amended_map_data


def write_catalogue_documents(documents: list[dict], county: str, version: str) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    publish_dir = PATH.PUBLISH / f"{county}/MAF73/{version}/"

    if publish_dir.exists():
        rmtree(publish_dir)
    publish_dir.mkdir(parents=True)
    for document in documents:
        with open(publish_dir / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"Record for farm {document['record']['citableReference']}: {final_file.name} DONE")
            json.dump(document, final_file)   


def write_jsons_to_zip_archive(county: str, version: str):
    logger.info(" ===== CREATING ZIP ARCHIVE ===== ")
    
    directory = PATH.PUBLISH / f"{county}/"
    archive_name = f"{directory}_MAF73"
    make_archive(
        archive_name,
        'zip',
        root_dir=PATH.PUBLISH,
        base_dir=f"{county}/MAF73/{version}",
    )
            
def process_proof_files(config: dict) -> None:
    xlsx_files = PATH.INPUT.glob("TEST/*MAF73*.xlsx") if config['test_mode'] else PATH.INPUT.glob("*MAF73*.xlsx")

    for proof_file in xlsx_files:
        if proof_file.name.startswith("Index"):
            continue
        county_code, _ = proof_file.name.split(" ", maxsplit=1)
        version = REGEX.TRANSCRIPTIONS_VERSION.match(proof_file.stem)['version']

        proof_data = load_excel_data(proof_file)
        map_data = clean_excel_data(proof_data)
        if (county_from_db := read_farms_db(county_code, config['test_mode'])) and 'MAF73' in county_from_db:
            existing_maps = county_from_db['MAF73'][version]
        else:
            existing_maps = {}
        map_data_with_ids = add_ids_to_maps(map_data, existing_maps)          
        final_documents = build_catalogue_documents(map_data_with_ids, config['update_scope'])
        if config['test_mode']:
            for document in final_documents:
                pretty.pprint(document)
        write_catalogue_documents(final_documents, county_code, version)
        write_jsons_to_zip_archive(county_code, version)
        logger.info("--- pausing for two minutes before next file ---")
        sleep(120)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    with open(Path(r"src/run_options.toml"), mode="rb") as fp:
        config = tomllib.load(fp)

    process_proof_files(config['map_publisher'])


if __name__ == "__main__":
    main(test_mode=False)

