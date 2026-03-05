import shelve

from src._config.constants import PATH


def process_forms(forms: dict) -> dict:
    output_forms = []
    output_files = []

    for form_type in forms.keys():
        if forms[form_type]:
            output_forms.append(form_type)
            for form in forms[form_type]:
                output_files.append(", ".join(form.images))
    return {
        'forms': ";\n".join(output_forms),
        'files': ";\n".join(output_files)
    }
    

def _transform_farm_to_proof(farm: Farm) -> list:
    forms_and_files = process_forms(farm.forms)
    return [
        farm.catalogue_reference,
        farm.warnings['Reference Warnings'],
        forms_and_files['files'],
        farm.warnings['Filename Warnings'],
        forms_and_files['forms'],
        farm.warnings['Type Warnings'],
        farm.primary_farm_number,
    ]


with shelve.open(PATH.TEST_DB, 'r') as farms_db:
    for county, references in farms_db.items():
        proof_data = [
            _transform_farm_to_proof(references[catalogue_reference]['Farm'])
            for catalogue_reference in references.keys()
        ]


