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




