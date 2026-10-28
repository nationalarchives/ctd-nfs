from src._dataclasses.farm_combine import HarvestedFarm
from src._tools.constants import PATH, REGEX
from src._tools.helpers import clean_excel_data, load_excel_data
from src._tools.logging_setup import create_logger
from src.farm_harvester import write_farms_to_db

logger = create_logger("src._config", "logging.yaml")


for out_file in PATH.HARVEST.glob("RD*.xlsx"):
    county, _ = out_file.name.split("_", maxsplit=1)
    logger.info(f"RESURRECTING {county}")
    county_code, _ = out_file.name.split(" ", maxsplit=1)
    version = REGEX.TRANSCRIPTIONS_VERSION.match(out_file.stem)['version']

    excel_data = load_excel_data(out_file)
    farm_data = clean_excel_data(excel_data)

    farms_for_db = {}
    for counter, farm in enumerate(farm_data):
        _, parish, farm_number = farm['farm_number'].split("/", maxsplit=2)
        resurrected_farm = HarvestedFarm(county, parish, farm_number)
        resurrected_farm.id = farm['farm_id']
        resurrected_farm.replica_id = farm['replica_id']
        logger.info(f"Resurrected {resurrected_farm.farm_reference}")
        farms_for_db.update({resurrected_farm.catalogue_reference: resurrected_farm})        

    write_farms_to_db(farms_for_db, county_code, version)
