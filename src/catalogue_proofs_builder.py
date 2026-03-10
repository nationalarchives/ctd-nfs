import shelve
import re
import logging

from src._config.constants import PATH, CSVEXCEL
from src.farm_setup import Farm, Details, ListOrStr
from src.details_still import distill_details
from src._tools.xlwriter import ExcelWriter


logger = logging.getLogger(__name__)


def process_forms(forms: dict) -> dict:
    output_forms = []
    output_files = []
    dates = {'field_info_date': [], 'primary_record_date': []}

    for form_type in forms.keys():
        if not forms[form_type]:
            continue
        output_forms.append(form_type)
        for form in forms[form_type]:
            output_files.append(", ".join(form.images))
            dates['field_info_date'].append(form.field_info_date)
            dates['primary_record_date'].append(form.primary_record_date)


    return {
        'forms': ";\n".join(output_forms),
        'files': ";\n".join(output_files),
        'dates': dates,
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


def create_full_name_and_address(Detail: Details) -> dict:
    full_name = process_names(Detail.title, Detail.individual_name, Detail.group_names)
    distilled_address = process_detail(Detail.address)
    
    name_is_single_value: bool = full_name['name'] != "[not specified]" and not re.search(r"""(;\n| \| )""", full_name['name'])
    address_is_single_value: bool = distilled_address != "[not specified]" and not re.search(r"""(;\n| \| )""", distilled_address)
    full_detail = f"{full_name['name']}, {distilled_address}" if name_is_single_value and address_is_single_value else ""
    
    return full_name | {'address': distilled_address, 'detail': full_detail}


def _transform_farm_to_proof(farm: Farm) -> list:
    print(f"\t{farm.catalogue_reference=}")
    forms_and_files_and_dates = process_forms(farm.forms)

    addressee = create_full_name_and_address(farm.addressee)
    farmer = create_full_name_and_address(farm.farmer)
    owner = create_full_name_and_address(farm.owner)
 
    return [
        farm.catalogue_reference,
        process_warnings(farm.warnings['Reference Warnings']),
        forms_and_files_and_dates['files'],
        process_warnings(farm.warnings['Filename Warnings']),
        forms_and_files_and_dates['forms'],
        process_warnings(farm.warnings['Type Warnings']),
        farm.farm_reference,
        process_detail(farm.farm_name),
        addressee['name'],
        addressee['warning'],
        addressee['address'],
        addressee['detail'],
        farmer['name'],
        farmer['warning'],
        farmer['address'],
        farmer['detail'],
        owner['name'],
        owner['warning'],
        owner['address'],
        owner['detail'],
        process_detail(farm.acreage),
        process_detail(farm.OS_map_sheet),
        process_detail(forms_and_files_and_dates['dates']['field_info_date']),
        process_detail(forms_and_files_and_dates['dates']['primary_record_date']),
    ]


def create_proof_files():
    with shelve.open(PATH.TEST_DB, 'r') as farms_db:
        for county, references in farms_db.items():
            print(f"{county=}")
            if county == 'RD Rutland':
                continue

            proof_data = [
                _transform_farm_to_proof(references[catalogue_reference]['Farm'])
                for catalogue_reference in references.keys()
            ]
            print(f"\tTotal farms = {len(proof_data)}")
            
            excel_data = [{
                'sheet_name': f"{county} Proof data",
                'row_data': proof_data,
                'column_settings': CSVEXCEL.PROOF_COLUMNS,
            }]
            
            proof_file_name = PATH.HARVEST / f"{county} Proof data.xlsx"
            xlwriter = ExcelWriter()
            xlwriter.write_excel(excel_data, proof_file_name)


if __name__ == "__main__":
    create_proof_files()