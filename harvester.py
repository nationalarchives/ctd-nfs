from src.harvester.file_processor import process_csv_files
from src.harvester.catalogue_proofs_builder import create_proof_files
from src._tools.logging_setup import create_logger


logger = create_logger("src._config", "logging.yaml")


def main():
    logger.info(" ===== HARVESTING FARMS ===== ")
    process_csv_files()

    # logger.info(" ===== CREATING PROOF FILES ===== ")
    # create_proof_files()


if __name__ == "__main__":
    main()

