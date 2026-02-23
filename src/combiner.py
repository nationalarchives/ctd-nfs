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
working_addresses = []

for idx, address in enumerate(sorted_addresses):
    print(f"{idx=}\t{address=}")
    if address == sorted_addresses[-1:][0]:
        working_addresses.append(address)
        continue

    other_addresses = sorted_addresses[idx + 1:]
    if not any([(address in target_address) for target_address in other_addresses]):
        working_addresses.append(address)

pretty.pprint(working_addresses)