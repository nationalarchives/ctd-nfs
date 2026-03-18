import re


def distill_single_name_and_address(name: str, address: str) -> str:
    if (name == "[not specified]" == address):
        return "[not specified]"

    if address == "[not specified]":
        return f"{name}"

    if (name != "[not specified]" != address) or (name == "[not specified]"):
        return f"{name}, {address}"


def distill_single_title_and_name(title: str, name: str) -> str:
    if (title == "[not specified]" == name) or (name == "[not specified]"):
        return "[not specified]"

    if (title != "[not specified]" != name):
        return f"{title} {name}"
    
    if (title == "[not specified]"):
        return f"{name}"


def distill_multiple_details(names: str, address: str) -> str:
    separated_names = re.split("; *", names)
    separated_addresses = re.split("; *", address)

    details = [
        distill_single_name_and_address(name, address)
        for name, address in zip(separated_names, separated_addresses)
    ]

    return "; ".join(details)


