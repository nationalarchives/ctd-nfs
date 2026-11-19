"""
@created: 2026-11-09
@author: Ralph Bruno

!!! THIS IS A NONCE SCRIPT - DO NOT RUN AFTER 2026-11-11

This will change the structure of the cache 
Currently:
<county-code>: {
    'V1': {
        <catalogue_reference>: <farm_instance>,
        ...
        }
    },
    'MAF73': {
        'V1': {
            <catalogue_reference: <map_dict>,
            ...
            }
        }
    }
}

this will be changed to:
<county-code>: {
    'MAF32': {
        'V1': {
            <catalogue_reference>: <farm_instance>,
            ...
            }
        }
    },
    'MAF73': {
        'V1': {
            <catalogue_reference: <map_dict>,
            ...
            }
        }
    }
}

"""

import pprint
import shelve
from datetime import date
from random import choice

from src._tools.constants import DB

pretty = pprint.PrettyPrinter(indent=4)


def add_MAF32_key() -> None:
    """
    For each county-code key in the cache, reassign the V1 data (dictionary mapping catalogue references to farm instances) to be a value of a MAF32 key
    """
    with shelve.open(DB.PRODUCTION, 'c') as cache:
        for county_code in cache:
            if county_code == 'AY':
                """
                AY: does not have farm entries yet
                """
                continue
            if county_code in ['GN', 'IW Isle of Wight', 'RD Rutland']:
                """
                GN: can be removed because no V1 data yet
                IW Isle of Wight: to be removed from cache - superceded by 'IW' data
                RD Rutland: to be removed from cache - superceded by 'RD' data
                """
                del cache[county_code]
                continue
            print(f"Adding MAF32 key to {county_code}")
            county_data: dict = cache[county_code].copy()
            county_data['MAF32'] = {'V1': county_data['V1'].copy()}
            del county_data['V1']

            cache[county_code] = county_data.copy()


def confirm_restructure() -> None:
    """
    print out random farms and/or maps from each county in the cache to confirm restructure has worked
    """    
    with shelve.open(DB.PRODUCTION, 'r') as cache:
        for county_code in cache:
            print(f"Reading random entries from {county_code}")

            county_data = cache[county_code].copy()
            if county_code != 'AY': 
                # MAF32 data not yet created for AY
                pretty.pprint(choice(list(county_data['MAF32']['V1'].values())).primary_farm_number)
            if county_code not in ['BN', 'IW', 'RD']: 
                # MAF73 entries not yet created/added for BN, IW, RD
                pretty.pprint(object=choice(list(county_data['MAF73']['V1'].values()))['id'])


def initialise_counties_in_cache() -> None:
    """Create entries for each county in the cache

    For counties which have yet to be harvested, create an dictionary in the cache with 'MAF32' & 'MA73' keys
    populated with empty dictionaries as values
    """
    county_codes: set[str] = {
        piece_row['County Code']
        for piece_row in DB.PIECES
    }
    pretty.pprint(county_codes)

    with shelve.open(DB.TEST, 'c') as cache:
        for _code in county_codes:
            print(f"Initialising {_code}")  
            cache[_code] = {'MAF32': {}, 'MAF73': {}}
            pretty.pprint(cache[_code])


restructure = {
    # dispatch table
    'add': add_MAF32_key,
    'check': confirm_restructure,
    'initialise': initialise_counties_in_cache,
}


if __name__ == "__main__":
    if date.today() == date(2026, 11, 19):
        restructure['initialise']()

