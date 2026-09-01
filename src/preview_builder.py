"""
"""
import pprint
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from _dataclasses.farm_record import DiscoveryMAF32
from src._tools.constants import PATH
from src._tools.helpers import clean_excel_data, load_excel_data
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def write_html_page(context: dict, county: str) -> None:
    environment = Environment(
        loader=FileSystemLoader("src/_html/"),
        autoescape=select_autoescape(enabled_extensions=('html', 'xml'),
                                     default_for_string=True,)
        )
    previews_template = environment.get_template("previews.html")
    previews_file = PATH.HARVEST / f"{county}_MAF32 previews.html"
    with open(previews_file, mode="w", encoding="utf-8") as results:
        results.write(previews_template.render(context))
        logger.info(f"... wrote {county}_MAF32 previews.html")


def create_html_preview_context(cleaned_data: list[dict], county: str) -> dict:
    """This will build a WYSIWYG preview page of the description portion of the Discovery record for each farm in the county

    Arguments:
        farm_instances -- farm instances retrieved from the farms db
        county -- name of the county in format <CODE> <Name> e.g., "RD Rutland"
    """
    MAF32_instances = [
        DiscoveryMAF32(proof)
        for proof in cleaned_data
    ]

    descriptions = [
        {
            'catalogue_reference': _inst.farm['catalogue_reference'],
            'farm_reference': _inst.farm['farm_number'],
            'farm_name': _inst.farm['farm_name'],
            'addressee': _inst.farm['addressee'],
            'farmer': _inst.farm['farmer'],
            'landowner': _inst.farm['landowner'],
            'acreage': _inst.farm['acreage'],
            'OS_map_sheet': _inst.farm['os_sheet_number'],
            'field_info_date': _inst.farm['field_info_date'],
            'primary_record_date': _inst.farm['primary_record_date'],
            'forms': _inst.farm['forms'],
        }
        for _inst in MAF32_instances
    ]

    catalogue_references = [
        _inst.farm['catalogue_reference']
        for _inst in MAF32_instances
    ]

    return {
        'descriptions_list': descriptions,
        'county': county,
        'references': catalogue_references,
    }
           
            
def create_html_preview(proof_file_name: str, excel_data=None, test_mode: bool=False) -> None:
    county, _ = proof_file_name.split("_", maxsplit=1)
    
    proof_data = load_excel_data(proof_file_name) if not excel_data else excel_data
    
    cleaned_data = clean_excel_data(proof_data)
    context = create_html_preview_context(cleaned_data, county)
    write_html_page(context, county)


def main(test_mode: bool=False):
    logger.info(" ===== PROCESSING PROOF FILES ===== ")
    xlsx_files = PATH.HARVEST.glob("TEST/*_MAF32 proof_*.xlsx") if test_mode else PATH.HARVEST.glob("*_MAF32 proof_*.xlsx")

    for proof_file in xlsx_files:
        create_html_preview(proof_file)


if __name__ == "__main__":
    main(test_mode=False)

