from containers import make_warnings_mapping, make_forms_mapping, Farm
from pre_instantiation_checks import perform_pre_instantiation_checks


def check_and_instantiate_farm(raw_farm_data: dict) -> Farm:
    """
    Perform pre-instantiation checks on raw farm data and instantiate a Farm object if checks pass.
    If checks fail, raise ValueError with appropriate message.

    Args:
        raw_farm_data (dict): dictionary containing raw farm data from CSV

    Returns:
        Farm: instantiated Farm object
    """
    
    warnings = perform_pre_instantiation_checks(stripped_data)

    farm = Farm(stripped_data)

    if warnings != "Pass":
        raise ValueError(f"Pre-instantiation checks failed with warnings: {warnings}")

    return farm

