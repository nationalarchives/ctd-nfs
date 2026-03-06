import shelve

from src._config.constants import PATH, CSVEXCEL
from src.farm_setup import Farm, ListOrStr
from src.details_still import distill_details
from src._tools.xlwriter import ExcelWriter


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
    

def process_detail(detail: ListOrStr) -> str:
    return detail if type(detail) is str else distill_details(detail)    


def process_warnings(warnings: list) -> str:
    return ";\n".join(warnings) or ""


def _transform_farm_to_proof(farm: Farm) -> list:
    print(f"\t{farm.catalogue_reference=}")
    forms_and_files = process_forms(farm.forms)

    return [
        farm.catalogue_reference,
        process_warnings(farm.warnings['Reference Warnings']),
        forms_and_files['files'],
        process_warnings(farm.warnings['Filename Warnings']),
        forms_and_files['forms'],
        process_warnings(farm.warnings['Type Warnings']),
        farm.farm_reference,
        process_detail(farm.farm_name),
        process_detail(farm.addressee.address),
        process_detail(farm.farmer.address),
        process_detail(farm.owner.address),
    ]


with shelve.open(PATH.TEST_DB, 'r') as farms_db:
    for county, references in farms_db.items():
        print(f"{county=}")
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

