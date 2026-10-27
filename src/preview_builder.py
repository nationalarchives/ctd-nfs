"""
"""
import pprint
from collections.abc import Generator
from pathlib import Path
from shutil import copy

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src._dataclasses.farm_combine import FarmForReview, HarvestedFarm
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


def create_html_preview_context(harvested_farms: Generator[HarvestedFarm], county: str) -> dict:
    """This will build a WYSIWYG preview page of the description portion of the Discovery record for each farm in the county

    Arguments:
        farm_instances -- farm instances retrieved from the farms db
        county -- name of the county in format <CODE> <Name> e.g., "RD Rutland"
    """

    farms_for_preview = (
        FarmForReview(harvested_farm)
        for harvested_farm in harvested_farms
    )

    descriptions = [
        {
            'catalogue_reference': preview_farm.catalogue_reference,
            'farm_reference': preview_farm.farm_reference,
            'farm_name': preview_farm.all_farm_names,
            'addressee': preview_farm.all_addressees,
            'farmer': preview_farm.all_farmers,
            'landowner': preview_farm.all_landowners,
            'acreage': preview_farm.all_acreages,
            'OS_map_sheet': preview_farm.all_os_sheet_numbers,
            'field_info_date': preview_farm.all_field_info_dates,
            'primary_record_date': preview_farm.all_primary_record_dates,
            'forms': preview_farm.all_forms,
        }
        for preview_farm in farms_for_preview
    ]

    catalogue_references = [
        preview_farm.catalogue_reference
        for preview_farm in farms_for_preview
    ]

    return {
        'descriptions_list': descriptions,
        'county': county,
        'references': catalogue_references,
    }
           
            
def create_html_preview(proof_file: Path, harvested_farms: dict) -> None:
    county, _ = proof_file.name.split("_", maxsplit=1)
    
    context = create_html_preview_context(harvested_farms.values(), county)

    previews_file_name = f"{proof_file.name.replace('_HarvesterOUT_', '_DiscoveryPreviews_').replace('xlsx', 'html')}"
    write_html_page(context, county, Path(proof_file.parent/ previews_file_name))
    copy(Path("src/_html/descriptions.js"), Path(proof_file.parent / "descriptions.js"))
    copy(Path("src/_html/style.css"), Path(proof_file.parent / "style.css"))


def main(test_mode: bool=False):
    logger.info("*** PROCESSING PROOF FILES ***")
    xlsx_files = PATH.HARVEST.glob("TEST/*_HarvesterOUT_*.xlsx") if test_mode else PATH.HARVEST.glob("*_HarvesterOUT_*.xlsx")

    for proof_file in xlsx_files:
        create_html_preview(proof_file)


if __name__ == "__main__":
    main(test_mode=False)

