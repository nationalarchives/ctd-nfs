import shelve
import logging

from src._tools.constants import PATH, DATA, DISCOVERY
from src._dataclasses.farm_model import Farm, Details
from src.publisher.record_setup import Image, Record, Replica


logger = logging.getLogger(__name__)


def _get_farm_instance(catalogue_reference: str) -> Farm:
    # TODO: parse county from filename
    county_name = "RD Rutland"
    with shelve.open(PATH.FARMS_DB, "r") as farms_db:
        return farms_db[county_name][catalogue_reference]['farm']


def create_description(row_data: dict) -> str:
    description = [
        f"{description_key}: {row_data[proof_key]}<p>"
        for proof_key, description_key in DATA.DESCRIPTION_FIELDS.items()
    ]

    return "".join(description)


def build_record_subdocument(farm_iaid: str, row: dict) -> Record:
    record = Record(
            iaid=farm_iaid,
            citableReference=row['catalogue_reference'],
        )
    record.scopeContent['description'] = create_description(row)

    return record


def build_replica_subdocument(forms: list, replica_id: str) -> Replica:
    replica_files = []
    files = [
        Image(originalName=image.name, id=image.id)
        for each_form in forms
        for image in each_form.images
    ]
    replica_files.extend(files)
        
    return Replica(
        replicaId=replica_id,
        files=replica_files
    )


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

        record = build_record_subdocument(farm.iaid, row)
        record: dict = eval(repr(record))      

        replica = build_replica_subdocument(farm.forms, record['replicaId'])
        replica: dict = eval(repr(replica))
        
        logger.info(f"Farm {farm.catalogue_reference} --> Built record {record['iaid']} with {len(replica['files'])} images")
        documents.append({'record': record, 'replica': replica})

    return documents

