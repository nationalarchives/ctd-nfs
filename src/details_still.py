"""
Merge list of names and address strings into one final version that will be visible in Discovery.
"""

from collections import Counter
import pprint


pretty = pprint.PrettyPrinter(indent=4)

# counts = Counter(list_of_addresses)


def prepare_details_for_filtration(harvested_details: list) -> list:
    cleaned_details = [item for item in harvested_details if item != "[not specified]"]
    unique_details = list(set(cleaned_details))
    return sorted(unique_details, key=len)


def filter_details(unique_details_sorted_by_length: list) -> list:
    working_details = []
    for idx, detail in enumerate(unique_details_sorted_by_length):
        if detail == unique_details_sorted_by_length[-1]:
            working_details.append(detail)
            continue

        other_addresses = unique_details_sorted_by_length[idx + 1:]
        if not any([(detail in target_address) for target_address in other_addresses]):
            working_details.append(detail)
   
    return working_details


def filter_details_by_line(details_after_first_filer: list) -> list:
    filtered_details = details_after_first_filer.copy()
    for idx, detail in enumerate(details_after_first_filer):
        if detail == details_after_first_filer[-1]:
            continue

        other_details = details_after_first_filer[idx + 1:]
        for target_detail in other_details:
            if all([(line in target_detail) for line in detail.split(", ")]):
                filtered_details.remove(detail)
                continue
    
    return filtered_details
    

def distill_details(list_of_details: list) -> str:
    sorted_details = prepare_details_for_filtration(list_of_details)
    working_details = filter_details(sorted_details)
    distilled_details = filter_details_by_line(working_details)

    return distilled_details[0] if len(distilled_details) == 1 else " / ".join(sorted(distilled_details))


