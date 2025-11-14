def generate_references(filenames: list[str], primary_farm_number: str, additional_farms: str, form: str, row_num: int, existing_refs: list[str]) -> tuple[dict[str, str], set[str]]:
    """
    Creates a catalogue reference for each farm in the required format: "MAF 32/<box number>/<parish number>/<farm number>"
    box number and parish number will be parsed from filename
    If reference can't be created due to missing data, a warning is added to the warnings set

    Args:
        filenames (list[str]): box number parsed from filename
        primary_farm_number (str): usually a number, can also be number/number e.g. "16/1", or "*"
        additional_farms (str): identifier of additional farms, semi-colon separated if multiple
        form (str): one of 'C51/SSY', 'B496/EI', 'C 47/SSY', 'C 49/SSY', 'SF', 'SF C69/SSY', 'Other', 'Cover'
        row_num (int): row number in the source spreadsheet
        existing_refs (list[str]): 

    Returns:
        tuple[dict[str, str], set[str]]: a list of generated references and a list of warnings
    """
    
    ref_list = {}
    warnings = set()
    
    if primary_farm_number == "*":
        ref = generate_ref("MAF 32/" + box_number + "/" + form, existing_refs)
        ref_list[ref] = form
        
    elif primary_farm_number != "" and additional_farms == "":
        ref = generate_ref("MAF 32/" + box_number + "/" + primary_farm_number, existing_refs)           
        ref_list[ref] = "Primary"
       
    elif primary_farm_number == "" and additional_farms != "":
        for additional_farm in additional_farms.split(";"):
            ref = generate_ref("MAF 32/" + box_number + "/" + additional_farm.strip(), existing_refs)           
            ref_list[ref] = "Additional"
        warnings.add("Row " + row_num + ": Error - Additional farm but no primary farm given")
        
    elif primary_farm_number != "" and additional_farms != "":
        ref = generate_ref("MAF 32/" + box_number + "/" + primary_farm_number, existing_refs)           
        ref_list[ref] = "Primary"
        
        for additional_farm in additional_farms.split(";"):
            ref = generate_ref("MAF 32/" + box_number + "/" + additional_farm.strip(), existing_refs)           
            ref_list[ref] = "Additional"          
               
        warnings.add("Row " + row_num + ": Warning - Additional farms present")
    elif form != "Other" or form != "Cover":        
        warnings.add("Row " + row_num + ": Note - type is " + form.lower() + " so no farm number specified")
        ref = generate_ref("MAF 32/" + box_number + "/" + form, existing_refs)
        ref_list[ref] = form
   
    if type == "Cover" and primary_farm_number != "*":
        warnings.add("Row " + row_num + ": Error - Type is cover and farm number is specified")
        ref = generate_ref("MAF 32/" + box_number + "/" + form, existing_refs)
        ref_list[ref] = form
               
    return (ref_list, warnings)  
