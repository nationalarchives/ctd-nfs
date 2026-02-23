"""
Merge list of names and address strings into one final version that will be visible in Discovery.
"""

from collections import Counter
import pprint


pretty = pprint.PrettyPrinter(indent=4)

list_of_addresses = [
	# "The Hall, Edith Weston",
	# "The Hall, Ashburton, Edith Weston",
	# "The Hall, Ashburton, Rutland",
	# "The Hall, Ashburton, Edith Weston, Rutland",
    # "Ashwell, Oakham, Rutland",
    # "Baines Farm, Ashwell, Oakham, Rutland",
    # "Baines Farm, Ashwell, Oakham, Rutland",
    "Westfield Cottage, Ashwell, Grange, Oakham",
    "c/o Capt Hornsby, Westfield Cottage, Ashwell, Oakham, Rutland",
    "c/o Capt Hornsby, Westfield Cottage, Ashwell, Oakham, Rutland",
]
counts = Counter(list_of_addresses)


def prepare_addresses_for_filtration(harvested_addresses: list) -> list:
    unique_addresses = list(set(list_of_addresses))
    return sorted(unique_addresses, key=len)


def filter_addresses(unique_addresses_sorted_by_length: list) -> list:
    working_addresses = []
    for idx, address in enumerate(unique_addresses_sorted_by_length):
        print(f"{idx=}\t{address=}")
        if address == unique_addresses_sorted_by_length[-1]:
            working_addresses.append(address)
            continue

        other_addresses = unique_addresses_sorted_by_length[idx + 1:]
        if not any([(address in target_address) for target_address in other_addresses]):
            working_addresses.append(address)
   
    return working_addresses


def filter_addresses_by_line(addresses_after_first_filer: list) -> list:
    filtered_addresses = addresses_after_first_filer.copy()
    for idx, address in enumerate(addresses_after_first_filer):
        if address == addresses_after_first_filer[-1]:
            continue

        other_addresses = addresses_after_first_filer[idx + 1:]
        for target_address in other_addresses:
            if all([(line in target_address) for line in address.split(", ")]):
                filtered_addresses.remove(address)
                continue
    
    return filtered_addresses


def distill_addresses(list_of_addresses: list) -> list:
    sorted_addresses = prepare_addresses_for_filtration(list_of_addresses)
    working_addresses = filter_addresses(sorted_addresses)
    distilled_addresses = filter_addresses_by_line(working_addresses)
    print(distilled_addresses)

    return distilled_addresses