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


def join_title_and_name(title: str, name: str) -> str:
    if "[not specified]" in [title, name]:
        return name

    elif title.startswith("Esq"):
        return f"{name} {title}"

    else:
        return f"{title} {name}"


def process_full_individual_name(titles: ListOrStr, individual_names: ListOrStr) -> str:
    if type(titles) is str and type(individual_names) is str:
        return join_title_and_name(titles, individual_names)

    full_names = []
    for index, title in enumerate(titles):
        name = individual_names[index]
        full_names.append(join_title_and_name(title, name))
    
    return distill_details(full_names)


def process_names(title: ListOrStr, individual_name: ListOrStr, group_names: ListOrStr) -> dict:
    individual_name = process_full_individual_name(title, individual_name)
    group_names = process_detail(group_names)

    if individual_name != "[not specified]" and group_names == "[not specified]":
        return {'name': individual_name, 'warning': ""}
    
    if individual_name == "[not specified]" and group_names != "[not specified]":
        return {'name': group_names, 'warning': ""}

    if individual_name == "[not specified]" and group_names == "[not specified]":
        return {'name': "[not specified]", 'warning': ""}
    
    if individual_name != "[not specified]" and group_names != "[not specified]":
        return {
            'name': f"{individual_name};\n{group_names}",
            'warning': "ERROR: farm contains both individual & group names - both names have been returned for inspection"
            }


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
        process_full_individual_name(farm.addressee.title, farm.addressee.individual_name),
        process_detail(farm.addressee.group_names),
        process_detail(farm.addressee.address),
        process_full_individual_name(farm.farmer.title, farm.farmer.individual_name),
        process_detail(farm.farmer.group_names),
        process_detail(farm.farmer.address),
        process_full_individual_name(farm.owner.title, farm.owner.individual_name),
        process_detail(farm.farmer.group_names),
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

