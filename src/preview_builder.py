"""
"""
import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src._dataclasses.farm_combine import HarvestedFarm, PublishedFarm
from src._dataclasses.farm_record import DiscoveryMAF32
from src._tools.constants import PATH
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


pretty = pprint.PrettyPrinter(indent=4)


def write_html_page(context: dict, county: str, previews_file: str) -> None:
    environment = Environment(
        loader=FileSystemLoader("src/_html/"),
        autoescape=select_autoescape(enabled_extensions=('html', 'xml'),
                                     default_for_string=True,)
        )
    previews_template = environment.get_template("previews.html")
    with open(PATH.HARVEST / previews_file, mode="w", encoding="utf-8") as results:
        results.write(previews_template.render(context))
        logger.info(f"... wrote {previews_file}")


def create_html_preview_context(farms: list[HarvestedFarm], county: str) -> dict:
    """This will build a WYSIWYG preview page of the description portion of the Discovery record for each farm in the county

    Arguments:
        farm_instances -- farm instances retrieved from the farms db
        county -- name of the county in format <CODE> <Name> e.g., "RD Rutland"
    """
    discovered_farms = [
        DiscoveryMAF32(PublishedFarm(harvested_farm))
        for harvested_farm in farms
    ]

    descriptions = [
        {
            'catalogue_reference': _farm.farm['catalogue_reference'],
            'farm_reference': _farm.farm['farm_number'],
            'farm_name': _farm.farm['farm_name'],
            'addressee': _farm.farm['addressee'],
            'farmer': _farm.farm['farmer'],
            'landowner': _farm.farm['landowner'],
            'acreage': _farm.farm['acreage'],
            'OS_map_sheet': _farm.farm['os_sheet_number'],
            'field_info_date': _farm.farm['field_info_date'],
            'primary_record_date': _farm.farm['primary_record_date'],
            'forms': _farm.farm['forms'],
        }
        for _farm in discovered_farms
    ]

    catalogue_references = [
        _farm.farm['catalogue_reference']
        for _farm in discovered_farms
    ]

    return {
        'descriptions_list': descriptions,
        'county': county,
        'references': catalogue_references,
    }
           
            
def create_html_preview(proof_file_name: str, farms: list[HarvestedFarm]) -> None:
    county, _ = proof_file_name.split("_", maxsplit=1)
    
    # proof_data = load_excel_data(proof_file_name) if not excel_data else excel_data
    
    # cleaned_data = clean_excel_data(proof_data)
    context = create_html_preview_context(farms, county)

    previews_file_name = f"{proof_file_name.replace('_HarvesterOUT_', '_DiscoveryPreviews_')}.html"
    write_html_page(context, county, previews_file_name)


def main(test_mode: bool=False):
    logger.info("*** PROCESSING PROOF FILES ***")
    xlsx_files = PATH.HARVEST.glob("TEST/*_HarvesterOUT_*.xlsx") if test_mode else PATH.HARVEST.glob("*_HarvesterOUT_*.xlsx")

    for proof_file in xlsx_files:
        create_html_preview(proof_file)


if __name__ == "__main__":
    main(test_mode=False)

