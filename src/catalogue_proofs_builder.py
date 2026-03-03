""""""
from pathlib import Path

from src.farm_setup import Farm
from src._tools.xlwriter import ExcelWriter
from src._config.constants import PATH, CSVEXCEL


def create_proofs_data(farm: Farm):
    filenames = []
    
    for forms in farm.forms.values():
        for form in forms:
            images = [image.name for image in form.images]
        filenames.append(", ".join(images))
    
    filenames = ";\n".join(filenames)             
    
    warnings = {key: "\n".join(farm.warnings[key]) for key in farm.warnings}

    return [
        farm.catalogue_reference,
        warnings['Reference Warnings'],
        filenames,
        warnings['Filename Warnings'],
        farm.document_type,
        warnings['Type Warnings'],
        farm.farm_reference,
        warnings['Farm Number Warnings'],
        farm.farm_name,
        warnings['Farm Name Warnings'],
        f"{farm}",
        warnings['Landowner Warnings'],
        warnings['Farmer Warnings'],
    ]



def create_proofs_data(_delivery_file: Path) -> dict:
    sheet_name = _delivery_file.name
    row_data = [
            create_proofs_item(concept)
            for concept in concepts
        ]
    return {
        'sheet_name': sheet_name,
        'row_data': row_data,
        'column_settings': CSVEXCEL.OUTPUT_COLUMNS,
    }


def make_proofs_file(_delivery_files: list) -> str:
    proofs_data = [
        create_proofs_data(each_file)
        for each_file in _delivery_files
    ]
    proofs_file_name = PATH.ARCHIVE / f"{county} Stage 2.xlsx"
    xlwriter = ExcelWriter()
    xlwriter.write_excel(proofs_data, proofs_file_name)
    return f"{proofs_file_name}"
