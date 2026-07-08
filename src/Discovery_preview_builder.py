"""
"""
import json
import pprint
import shelve
from pathlib import Path
import re
from typing import Iterator

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src._tools.constants import PATH
from src._tools.xlreader import read_file
from src._tools.logging_setup import create_logger
from src._dataclasses.MAF32_model import DiscoveryMAF32


logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def create_html_preview_context(cleaned_data: list[dict], county: str) -> dict:
    """This will build a WYSIWYG preview page of the description portion of the Discovery record for each farm in the county

    Arguments:
        farm_instances -- farm instances retrieved from the farms db
        county -- name of the county in format <CODE> <Name> e.g., "RD Rutland"
    """
    MAF32_instances = [
        DiscoveryMAF32(MAF32_instances)
        for MAF32_instances in cleaned_data
    ]

    descriptions = [
        {
            'catalogue_reference': proof.farm['catalogue_reference'],
            'farm_reference': proof.farm['farm_number'],
            'farm_name': proof.farm['farm_name'],
            'addressee': proof.farm['addressee'],
            'farmer': proof.farm['farmer'],
            'landowner': proof.farm['landowner'],
            'acreage': proof.farm['acreage'],
            'OS_map_sheet': proof.farm['os_sheet_number'],
            'field_info_date': proof.farm['field_info_date'],
            'primary_record_date': proof.farm['primary_record_date'],
            'forms': proof.farm['forms'],
        }
        for proof in cleaned_data
    ]

    farm_references = [
        proof.farm['farm_number']
        for proof in cleaned_data
    ]

    return {
        'descriptions_list': descriptions,
        'county': county,
        'references': farm_references,
    }


def write_html_page(context: dict, county: str) -> None:
    environment = Environment(
        loader=FileSystemLoader("src/_html/"),
        autoescape=select_autoescape(enabled_extensions=('html', 'xml'),
                                     default_for_string=True,)
        )
    previews_template = environment.get_template("previews.html")
    previews_file = PATH.HARVEST / f"{county}_scopeAndContent previews.html"
    with open(previews_file, mode="w", encoding="utf-8") as results:
        results.write(previews_template.render(context))
        logger.info(f"... wrote {county}_scopeAndContent previews.html")


def load_excel_data(data_file: Path) -> list[dict]:
    logger.info(F" ===== LOADING PROOF FILE {data_file.name}===== ")
    excel_data = read_file(data_file)

    column_names = excel_data['Proof data'][0]

    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data["Proof data"][1:]
        if row_data[0]
    ]


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
    logger.info(" ===== CLEANING PROOF DATA ===== ")
    discovery_data = []
    non_breaking_space = "\xa0"
    for row in raw_csv_data:
        cleaned_data_row = {}
        for key, value in row.items():
            if not value or type(value) is not str:
                cleaned_data_row[key] = value
                continue

            value = value.strip()
            value = value.replace(f"{non_breaking_space}", " ")
            value = value.replace("\n", "")
            value = re.sub(r";\s*", "; ", value)
            cleaned_data_row[key] = value

        discovery_data.append(cleaned_data_row)
    
    return discovery_data
           
            
def process_proof_files(test_mode: bool=False) -> None:
    xlsx_files = PATH.TEST_PUBLISH.glob("*.xlsx") if test_mode else PATH.PUBLISH.glob("*.xlsx")

    for proof_file in xlsx_files:
        county, _ = proof_file.name.split("_", maxsplit=1)
        proof_data = load_excel_data(proof_file)
        cleaned_data = clean_excel_data(proof_data)
        context = create_html_preview_context(cleaned_data, county)
        write_html_page(context, county)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    process_proof_files()


if __name__ == "__main__":
    main(test_mode=False)

