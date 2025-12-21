from pathlib import Path
import re

from farm_class_setup import Farm
from pre_instantiation_checks import validate_farm_reference_values
from constants import DATA, REGEX
from src.file_processor import convert_to_generator, load_data_from_file


CSV_FILES = Path(r"C:\Users\rbruno\OneDrive - The National Archives\Projects\NFS\Pipeline\1-INPUT")


if __name__ == "__main__":
    csv_files = CSV_FILES.glob("*.csv")

    for csv_file in csv_files:
        if csv_file.name != "Rutland Edited Data for RALPH.csv":
            continue
        cleaned_farm_data: list[dict] = load_data_from_file(csv_file)
        farm_data_generator = convert_to_generator(cleaned_farm_data)
        for farm_data_row in farm_data_generator:
            print(f"\nProcessing row {farm_data_row['row_number']} ...")
            pattern_matches: dict[re.Match] = {
                'filename_1': REGEX.FORM_PATTERN.match(farm_data_row['filename_1']),
                'filename_2': REGEX.FORM_PATTERN.match(farm_data_row['filename_2']),
                'cover': REGEX.COVER_PATTERN.match(farm_data_row['filename_1']),
            }
            row_prefix = f"Row {farm_data_row['row_number']}: "

            if not validate_farm_reference_values(farm_data_row, pattern_matches):
                continue

                warnings = perform_pre_instantiation_checks(farm_data_row)
            except Exception as check_exception_msg:
                print(f"{check_exception_msg}")
                continue

            candidate_farm = Farm(**farm_data_row)
            candidate_farm.warnings = warnings
            if candidate_farm.catalogue_reference not in Farm.all_farms:
                Farm.all_farms[candidate_farm.catalogue_reference] = candidate_farm
                print(f"Successfully instantiated Farm: {candidate_farm.catalogue_reference}")
            else:
                print(f"Catalogue reference {candidate_farm.catalogue_reference} already exists. Merging data ...")
                # existing_farm = Farm.all_farms[candidate_farm.catalogue_reference]
                # existing_farm.merge_with_another_farm(candidate_farm)
                # print(f"Successfully merged Farm: {candidate_farm.catalogue_reference}")
        # print(f"{Farm.all_farms=}")
