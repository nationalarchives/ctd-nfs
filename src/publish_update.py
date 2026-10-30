import tomllib
from pathlib import Path

from src._tools.constants import DB, PATH, REGEX
from src._tools.helpers import clean_excel_data, create_uuid_str, load_excel_data
from src._tools.logging_setup import create_logger
from src.farm_harvester import read_farms_db

logger = create_logger("src._config", "logging.yaml")


def process_proof_files(config: dict) -> None:
    xlsx_files = PATH.INPUT.glob("TEST/*MAF73*.xlsx") if config['test_mode'] else PATH.INPUT.glob("*MAF73*.xlsx")

    for proof_file in xlsx_files:
        county_code, _ = proof_file.name.split(" ", maxsplit=1)
        if (version := REGEX.TRANSCRIPTIONS_VERSION.match(proof_file.stem)['version']) in ["V0", "V1"]:
            logger.error("Input file version must be V2 or above")
            continue

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

