import re


def distill_single_name_and_address(title: str, name: str, address: str) -> str:
    full_name = distill_single_title_and_name(title, name)

    if (full_name == "[not specified]" == address):
        return "[not specified]"

    if address == "[not specified]":
        return f"{full_name}"

    if (full_name != "[not specified]" != address) or (full_name == "[not specified]"):
        return f"{full_name}, {address}"


def distill_single_title_and_name(title: str, name: str) -> str:
    if (title == "[not specified]" == name) or (name == "[not specified]"):
        return "[not specified]"

    if (title != "[not specified]" != name):
        if title.startswith(("Esq", "KC")):
            return f"{name}, {title}"
        return f"{title} {name}"
    
    if (title == "[not specified]"):
        return f"{name}"


def distill_multiple_details(titles: str, names: str, address: str) -> str:
    separated_titles = re.split("; *", titles)
    separated_names = re.split("; *", names)
    separated_addresses = re.split("; *", address)

    details = [
        distill_single_name_and_address(title, name, address)
        for title, name, address in zip(separated_titles, separated_names, separated_addresses)
    ]

    return "; ".join(details)


