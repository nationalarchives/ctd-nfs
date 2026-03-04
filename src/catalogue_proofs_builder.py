import shelve

from src._config.constants import PATH


with shelve.open(PATH.TEST_DB, 'r') as farms_db:
    for county, references in farms_db.items():
        for catalogue_reference in references.keys():
            farm = references[catalogue_reference]['Farm']
            
            pass
