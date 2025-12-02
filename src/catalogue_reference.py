def make_catalogue_reference(reference_data: dict[str]) -> str:
    """
    Creates a catalogue reference for each farm in the required csv_data['document_type']at: f"MAF 32/<box number>/<parish number>/<farm number>"
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
    
    # ref_list = {}
    warnings = set()
    
    # if primary_farm_number is "*":
    #   add document type to catalogue reference
    #   map catalogue reference to document type
    if reference_data['primary_farm_number'] == "*":
        reference = reference_data['document_type']
        # ref_list[ref] = csv_data['document_type']

    # else if primary farm number is given and no additional farms: 
    #   add primary farm number to catalogue reference
    #   map catalogue_reference to "Primary"
    elif reference_data['primary_farm_number'] and not reference_data['additional_farms']:
        reference = reference_data['primary_farm_number']
        # ref_list[ref] = "Primary"

    # else if no primary farm number but additional farms:
    #   for each additional farm:
    #       add additional farm to catalogue reference
    #       map catalogue reference to "Additional"
    #   add warning "Error - Additional farm but no primary farm given
    elif not reference_data['primary_farm_number'] and reference_data['additional_farms']:
        for additional_farm in reference_data['additional_farms'].split(";"):
            reference = additional_farm
            # ref_list[ref] = "Additional"

        warnings.add(f"Row {reference_data['row_num']}: Error - Additional farm but no primary farm given")

    # else if both primary farm number and additional farms:
    #   add primary farm number to catalogue reference
    #   map catalogue reference to "Primary"        
    #   for each additional farm:
    #       add additional farm to catalogue reference
    #       map catalogue reference to "Additional"
    #   add warning "Warnings - Additional farms present"
    elif reference_data['primary_farm_number'] and reference_data['additional_farms']:
        reference = reference_data['primary_farm_number']
        # ref_list[ref] = "Primary"

        for additional_farm in reference_data['additional_farms'].split(";"):
            reference = additional_farm
            # ref_list[ref] = "Additional"
        warnings.add(f"Row {reference_data['row_num']}: Warning - Additional farms present")
    
    # else if document_type is not 'Cover' or 'Other':
    #   add warning - "Note - type is document_type  so no farm number specified"
    #   add document type to catalogue reference
    #   map catalogue reference to document_type
    elif reference_data['document_type'] not in ["Other", "Cover"]:        
        warnings.add(f"Row {reference_data['row_num']}: Note - type is {reference_data['document_type'].lower()} so no farm number specified")
        reference = reference_data['document_type']
        # ref_list[ref] = csv_data['document_type']

    # else if document_type is 'Cover' and primary farm number is given:
    #   add warning - "Error - Type is cover and farm number is specified"
    #   add document type to catalogue reference
    #   map catalogue reference to document_type
    if reference_data['document_type'] == "Cover" and reference_data['primary_farm_number'] != "*":
        warnings.add(f"Row {reference_data['row_num']}: Error - Type is cover and farm number is specified")
        reference = reference_data['document_type']
        # ref_list[ref] = csv_data['document_type']
              
    catalogue_reference = \
        f"MAF 32/" \
        f"{reference_data['box_number']}/" \
        f"{reference_data['parish_number']}/" \
        f"{reference}"

    return (catalogue_reference, warnings)
