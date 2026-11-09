"""
@created: 2026-11-09
@author: Ralph Bruno

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

import shelve

from src._tools.constants import DB

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
