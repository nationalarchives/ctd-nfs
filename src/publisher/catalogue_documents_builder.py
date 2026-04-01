import shelve
import logging

from src._tools.constants import PATH, DATA, DISCOVERY
from src.harvester.farm_setup import Farm
from src.publisher.record_setup import Image, Record, Replica


logger = logging.getLogger(__name__)


def _get_farm_instance(catalogue_reference: str) -> Farm:
    # TODO: parse county from filename
    county_name = "RD Rutland"
    with shelve.open(PATH.FARMS_DB, "r") as farms_db:
        return farms_db[county_name][catalogue_reference]['Farm']


def create_description(row_data: dict) -> str:
    description_values = {
        key: row_data[key]
        for key in DISCOVERY.DESCRIPTION_FIELDS
    }

    return DISCOVERY.DESCRIPTION_TEMPLATE.substitute(description_values)


def build_record_subdocument(farm_iaid: str, row: dict) -> Record:
    record = Record(
            iaid=farm_iaid,
            citableReference=row['catalogue_reference'],
        )
    record.scopeContent['description'] = create_description(row)

    return record


def build_replica_subdocument(forms: dict, replica_id: str) -> Replica:
    replica_files = []
    for list_of_forms in forms.values():
        if not list_of_forms:
            continue
        files = [
            Image(originalName=image.name, id=image.id)
            for form in list_of_forms
            for image in form.images
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
        if test_mode and row['catalogue_reference'] != "MAF 32/348/40/3a":
            continue

        farm = _get_farm_instance(row['catalogue_reference'])

        record = build_record_subdocument(farm.iaid, row)
        record: dict = eval(repr(record))      

        replica = build_replica_subdocument(farm.forms, record['replicaId'])
        replica: dict = eval(repr(replica))
        
        logger.info(f"--- Built record {record['iaid']} with {len(replica['files'])} images")
        documents.append({'record': record, 'replica': replica})

    return documents

