import shelve
import logging

from src._tools.constants import PATH
from src._dataclasses.farm_model import Farm, Details
from src._dataclasses.discovery_model import Discovery


logger = logging.getLogger(__name__)


def _get_farm_instance(catalogue_reference: str) -> Farm:
    # TODO: parse county from filename
    county_name = "RD Rutland"
    with shelve.open(PATH.FARMS_DB, "r") as farms_db:
        return farms_db[county_name][catalogue_reference]['farm']



def build_catalogue_documents(cleaned_data: list[dict], test_mode=False) -> list[dict]:
    logger.info(" ===== BUILDING DISCOVERY RECORDS ===== ")

    documents = []
    for row in cleaned_data:
        farm = _get_farm_instance(row['catalogue_reference'])
        farm.farm_name = row['farm_name']
        farm.landowner = Details(full_address=row['landowner'])
        farm.farmer = Details(full_address=row['farmer'])
        farm.addressee = Details(full_address=row['addressee'])
        farm.acreage = row['acreage']
        farm.OS_map_sheet = row['os_sheet_number']
        farm.field_info_date = row['field_info_date']
        farm.primary_record_date = row['primary_record_date']
        farm.additional_farms = row['additional_farms']

        discovery_document = Discovery(farm)
        logger.info(f"Farm {farm.catalogue_reference} --> Built record {farm.iaid} with {len(discovery_document.files)} images")
        
        documents.append(discovery_document.to_dict())

    return documents

