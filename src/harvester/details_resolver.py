import re
from itertools import zip_longest


def resolve_title_name_and_address(title: str, name: str, address: str) -> dict:
    has_title = title not in ["", "_null_", "_not transcribed_"]
    has_name = name not in ["_null_", "_not transcribed_"]

    if (has_title and has_name):
        full_name = f"{name} {title}" if title.startswith(("Esq", "KC")) else f"{title} {name}"

    elif not (has_title or has_name) or not has_name:
        full_name = "[not specified]"
    
    elif not has_title:
        full_name = name
    
    if address in ["_null_", "_not transcribed_"]:
        address = "[not specified]"

    return {'name': full_name, 'address': address}


def is_existing_detail(new_detail: dict, existing_details: list[dict]) -> bool:
    return any(
        new_detail['name'].lower() == detail['name'].lower() and new_detail['address'].lower() == detail['address'].lower() 
        for detail in existing_details
        )


def resolve_details(titles: list[str], individual_names: list[str], group_names: list[str], addresses: list[str]) -> tuple[list[dict], str]:
    warning = ""
    has_individual_names = any(
        name not in ["_null_", "_not transcribed_"]
        for name in individual_names
    )
    has_group_names = any(
        name not in ["_null_", "_not transcribed_"]
        for name in group_names
    )

    if len(individual_names) > 1 and has_individual_names and has_group_names:
        warning = "WARNING: Both individual & group names - both names have been returned for inspection"

    details = []
    for item in zip(titles, individual_names, group_names, addresses):
        title, name, group_name, address = item
        if group_name not in ["_null_", "_not transcribed_"]:
            name = group_name
            title = ""

        for _item in zip_longest(re.split("; *", title), re.split("; *", name), re.split("; *", address), fillvalue=""):
            _title, _name, _address = _item
            full_address: dict = resolve_title_name_and_address(_title, _name, _address)
            if not is_existing_detail(full_address, details):
                details.append(full_address)

    return details, warning
   
    