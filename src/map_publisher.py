import json
import pprint
import tomllib
from pathlib import Path
from shutil import rmtree

from _dataclasses.map_record import DiscoveryMAF73
from src._tools.constants import PATH
from src._tools.helpers import clean_excel_data, load_excel_data
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")
pretty = pprint.PrettyPrinter(indent=4)


def build_catalogue_documents(cleaned_data: list[dict], test_mode=False) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for map_proof in cleaned_data:
        map_document = DiscoveryMAF73(map_proof)

        logger.info(f"Farm {map_proof['Reference']} --> Built record {map_document.id} with {len(map_document.files)} images")

        documents.append(map_document.to_dict())
        # documents.append(map_document.for_index())

    return documents


def write_catalogue_documents(documents: list[dict], county: str) -> None:
    logger.info(" ===== WRITING DISCOVERY RECORDS ===== ")
    publish_dir = PATH.PUBLISH / f"{county}/MAF73/{version}/"

    if publish_dir.exists():
        rmtree(publish_dir)
    publish_dir.mkdir(parents=True)
    for document in documents:
        with open(publish_dir / f"{document['record']['iaid']}.json", 'w') as final_file:
            logger.info(f"Record for farm {document['record']['citableReference']}: {final_file.name} DONE")
            json.dump(document, final_file)   
            
def process_proof_files(config: dict) -> None:
    xlsx_files = PATH.INPUT.glob("TEST/*MAF73*.xlsx") if config['test_mode'] else PATH.INPUT.glob("*MAF73*.xlsx")

    for proof_file in xlsx_files:
        if proof_file.name.startswith("Index"):
            continue
        county_code, _ = proof_file.name.split(" ", maxsplit=1)
        version = REGEX.TRANSCRIPTIONS_VERSION.match(proof_file.stem)['version']

        proof_data = load_excel_data(proof_file)
        cleaned_data = clean_excel_data(proof_data)
        final_documents = build_catalogue_documents(cleaned_data, config['test_mode'])
        if config['test_mode']:
            for document in final_documents:
                pretty.pprint(document)
        write_catalogue_documents(final_documents, county_code)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    with open(Path(r"src/run_options.toml"), mode="rb") as fp:
        config = tomllib.load(fp)

    process_proof_files(config['map_publisher'])


if __name__ == "__main__":
    main(test_mode=False)

