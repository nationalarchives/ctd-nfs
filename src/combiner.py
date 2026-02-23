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

unique_addresses = list(set(list_of_addresses))
sorted_addresses = sorted(unique_addresses, key=len)


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


working_addresses = filter_addresses(sorted_addresses)
s2nd_working_group = working_addresses.copy()
for idx, address in enumerate(working_addresses):
    if address == working_addresses[-1]:
        continue

    other_addresses = working_addresses[idx + 1:]
    for target_address in other_addresses:
        if all([(line in target_address) for line in address.split(", ")]):
            s2nd_working_group.remove(address)
            continue

print(s2nd_working_group)