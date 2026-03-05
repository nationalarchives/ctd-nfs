import shelve

from src._config.constants import PATH, CSVEXCEL
from src.farm_setup import Farm


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
        ";\n".join(farm.warnings['Reference Warnings']) or "",
        forms_and_files['files'],
        ";\n".join(farm.warnings['Filename Warnings']) or "",
        forms_and_files['forms'],
        ";\n".join(farm.warnings['Type Warnings']) or "",
        farm.farm_reference,
    ]


with shelve.open(PATH.TEST_DB, 'r') as farms_db:
    for county, references in farms_db.items():
        proof_data = [
            _transform_farm_to_proof(references[catalogue_reference]['Farm'])
            for catalogue_reference in references.keys()
        ]
        
        excel_data = [{
            'sheet_name': f"{county} Proof data",
            'row_data': proof_data,
            'column_settings': CSVEXCEL.PROOF_COLUMNS,
        }]

        proof_file_name = PATH.OUTPUT / f"{county} Proof data.xlsx"
        xlwriter = ExcelWriter()
        xlwriter.write_excel(excel_data, proof_file_name)

