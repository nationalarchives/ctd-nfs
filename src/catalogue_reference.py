def make_catalogue_reference(reference_data: dict[str]) -> str:
    """
    Creates a catalogue reference for each farm in the required format: f"MAF 32/<box number>/<parish number>/<farm number>"
    box number and parish number will be parsed from filename
    If reference can't be created due to missing data, a warning is added to the warnings set
    •	The full catalogue reference as will be displayed in the catalogue
    •	There can only be one catalogue reference per farm. In some instances, this may not be the case. See warnings and checks for more information.
    Must begin “MAF 32”. See Overview of Catalogue structure for example. The piece/box number should be able to be extracted from the filename(s) in column A for most cases but not all.

    Args:
        reference_data (dict[str]): _description_

    Returns:
        str: _description_
    """
    
    warnings = {'Reference Warnings': ""}  
    primary_farm_number_missing: bool = reference_data['primary_farm_number'] == "*"

    if primary_farm_number_missing:
        farm_value = reference_data['document_type']
        is_a_primary_farm = False

    elif reference_data['primary_farm_number'] and not reference_data['additional_farms']:
        farm_value = reference_data['primary_farm_number']

    elif not reference_data['primary_farm_number'] and reference_data['additional_farms']:
        is_a_primary_farm = False
        additional_farms = []
        for additional_farm_number in reference_data['additional_farms']:
            farm_value = additional_farm_number
            additional_farms.append(additional_farm_number)
        warnings['Reference Warnings'] = f"Row {reference_data['row_num']}: Error - Additional farm but no primary farm given"

    elif reference_data['primary_farm_number'] and reference_data['additional_farms']:
        additional_farms = []
        farm_value = reference_data['primary_farm_number']
        for additional_farm_number in reference_data['additional_farms']:
            farm_value = additional_farm_number
            additional_farms.append(additional_farm_number)
        warnings['Reference Warnings'] = f"Row {reference_data['row_num']}: Warning - Additional farms present"
    
    elif reference_data['document_type'] not in ["Other", "Cover"]:        
        warnings['Reference Warnings'] = f"Row {reference_data['row_num']}: Note - type is {reference_data['document_type'].lower()} so no farm number specified"
        farm_value = reference_data['document_type']

    if reference_data['document_type'] == "Cover" and reference_data['primary_farm_number']:
        warnings['Reference Warnings'] = f"Row {reference_data['row_num']}: Error - Type is cover and farm number is specified"
        farm_value = reference_data['document_type']
              
    catalogue_reference = \
        f"MAF 32/" \
        f"{reference_data['box_number']}/" \
        f"{reference_data['parish_number']}/" \
        f"{farm_value}"

    return (
        {
            'catalogue_reference': catalogue_reference, 
            'is_a_primary_farm': is_a_primary_farm if 'is_a_primary_farm' in locals() else True,
            'additional_farms': additional_farms if 'additional_farms' in locals() else []
        }, 
        warnings)
