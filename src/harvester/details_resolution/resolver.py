import re


def resolve_single_name_and_address(title: str, name: str, address: str) -> dict:
    full_name = resolve_single_title_and_name(title, name)

    has_address = address not in ["[not specified]", "_not transcribed_"]
    has_full_name = full_name not in ["[not specified]", "_not transcribed_"]

    if not (has_full_name and has_address):
        return {'name': "[not specified]", 'address': "[not specified]"}

    if not has_address:
       return {'name': full_name, 'address': "[not specified]"}
    
    if (has_full_name and has_address) or not has_full_name:
        return {'name': full_name, 'address': address}


def resolve_single_title_and_name(title: str, name: str) -> str:
    has_title = title not in ["[not specified]", "_not transcribed_"]
    has_name = name not in ["[not specified]", "_not transcribed_"]

    if not (has_title and has_name) or not has_name:
        return "[not specified]"

    if (has_title and has_name):
        if title.startswith(("Esq", "KC")):
            return f"{name}, {title}"
        return f"{title} {name}"
    
    if not has_title:
        return f"{name}"


def resolve_multiple_details(titles: str, names: str, address: str) -> str:
    separated_titles = re.split("; *", titles)
    separated_names = re.split("; *", names)
    separated_addresses = re.split("; *", address)

    details = [
        resolve_single_name_and_address(title, name, address)
        for title, name, address in zip(separated_titles, separated_names, separated_addresses)
    ]

    return "; ".join(details)


