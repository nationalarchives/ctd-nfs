"""Utility helpers for data loading, validation, and cached lookups.

This module provides shared helper functions and lightweight value objects used
across the project for working with discovery and transcription data. It
centralises common tasks such as generating UUIDs, parsing semicolon-delimited
field values, reading spreadsheet content into dictionaries, normalising raw
data, resolving piece references, and retrieving cached county data.

Classes:
    TranscriptionDataError: Base exception for transcription/business-rule
        validation failures.
    ValueObject: Base class for simple value-based objects.

Functions:
    create_uuid_str(): Return a new random UUID as a string.
    split_list_values(field_value): Split a semicolon-delimited value into a
        list of cleaned strings.
    load_excel_data(data_file): Read spreadsheet data and convert a worksheet
        into a list of dictionaries keyed by column names.
    clean_excel_data(raw_csv_data): Strip extraneous whitespace and normalise
        line breaks and separators in raw row values.
    get_piece_value(county_code, parish_number): Look up a piece number using a
        county/parish key, with results cached for reuse.
    get_parent_discovery_record(ref_url_safe): Fetch a parent discovery record
        from the configured discovery API.
    read_county_data_from_cache(county_code, collection, test_mode=False):
        Read county-level cached farm or map data for the requested collection.

Example:
    piece_number = get_piece_value("RD", "123")
    county_data = read_county_data_from_cache("IW", "MAF32")
"""

import logging
import re
import shelve
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Literal

import requests

from src._tools.constants import DB, DISCOVERY
from src._tools.xlreader import read_file

logger = logging.getLogger(__name__)

def create_uuid_str():
    return f"{uuid.uuid4()}"


class TranscriptionDataError(Exception):
    """A base class for all business rule validation exceptions"""


class ValueObject:
    """A base class for all value objects"""


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value) if item != "*"]


def load_excel_data(data_file: Path) -> list[dict]:
    logger.info(F" ===== LOADING PROOF FILE {data_file.name}===== ")
    excel_data = read_file(data_file)

    column_names = excel_data['Sheet1'][0]

    return [
        dict(zip(column_names, row_data))
        for row_data in excel_data['Sheet1'][1:]
        if row_data[0]
    ]


def clean_excel_data(raw_csv_data: list[dict]) -> list[dict]:
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


@lru_cache
def get_piece_value(county_code: str, parish_number: str) -> str | None:
    all_references = (
        reference
        for reference in DB.PIECES
        if reference['County & Parish'] == f"{county_code}/{parish_number}"
    )
    reference: dict[str, str] | None = next(all_references, None)

    if reference is None:
        return None
    return reference['Piece Number']


@lru_cache
def get_parent_discovery_record(ref_url_safe: str) -> dict:
    api_query = fr"{DISCOVERY.API_URI}/records/v1/collection/{ref_url_safe}"
    # api_query = fr"{DISCOVERY.API_URI}/records/byref?reference={ref_url_safe}"
    result = requests.get(api_query)

    return result.json()


type CollectionName = Literal["MAF32", "MAF73"]

def read_county_data_from_cache(county_code: str, collection: CollectionName, test_mode: bool = False) -> dict:
    """Read cached county data for a given collection.

    This function loads the selected county's data from the production or test
    shelve cache and returns the records stored under the requested collection.
    The collection may represent farm data ("MAF32") or map data ("MAF73").

    Args:
        county_code: County code used as the cache key, for example "AB" or "XY".
        collection: Collection name to retrieve. Must be either "MAF32" or
            "MAF73".
        test_mode: If True, read from the test cache instead of the production
            cache.

    Returns:
        dict: A mapping of build version to records for the requested collection.
        For example:
            {"V1": {"MAF 32/850/354/27": <HarvestedFarm instance>}}
            {"V1": {"MAF 73/13/74/NW": <map dict>}}

    Raises:
        KeyError: If the county code does not exist in the selected cache.
    """
    with shelve.open(DB.TEST if test_mode else DB.PRODUCTION, 'r') as farm_db:
        county_data = farm_db[county_code].copy()

    return county_data[collection]

