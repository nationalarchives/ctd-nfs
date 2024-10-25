# Create a QA spreadsheet
# 
# Input Columns: filename_1, filename_2, document_type, county, parish, primary_farm_number, additional_farms, farm_name, addressee_title, addressee_individual_name, addressee_group_names, address, owner_title, owner_individual_name, owner_group_names, owner_address, farmer_title, farmer_individual_name, farmer_group_names, farmer_address, acreage, OS_map_sheet, field_info_date, primary_record_date
#    
# Output Columns: Expected Ref, Ref Warnings, Filenames, File Warnings, Type, Type Warnings, Farm Number, Farm Warnings, Farm Name, Farm Name Warnings, Landowner, Landowner Warnings, Farmer, Farmer Warnings, Acreage, OS Sheet Num, OS Warnings, Field Date, Field Date Warnings, Primary Date, Primary Date Warnings
#

# Need to match rows on filenames (before underscore) + farm number

import csv, re
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

def load_spreadsheet_data(processing_folder):
    ''' Process any csv files in the processing folder

        Keyword arguments:
            processing_folder - string with path to folder
        
        Returns:

    '''
    try: 
        for file in Path(processing_folder).glob("*.csv"):     
            
            base_filename = Path(file).stem
               
            with open(file, newline='') as f:
                values = csv.DictReader(f) 
                farm_values = extract_farms(values)  
                #print(farm_values)                
                
                output_excel(Path(processing_folder, "output", base_filename + ".xlsx"), farm_values)
                
    except OSError as e:
        print("Error in data loading: " + e)
        

def output_excel(output_file, values):
    wb = Workbook()
    sheet = wb.active
    
    headings = ["Reference", "Reference Warnings", "Filenames", "Filename Warnings", "Type", "Type Warnings"]
    default_widths = [20, 20, 30, 20, 15, 20]
    
    for i in range(0, len(headings)):
        column = headings[i]
        col_num = i+1
        
        sheet.cell(1, col_num, column).font = Font(bold=True)
        sheet.column_dimensions[get_column_letter(col_num)].width = default_widths[i]  
        
        row = 2
        for ref in values:
            sheet.cell(row, 1, ref)
            
            farm_values = values[ref]

            if column != "Reference" and column in farm_values.keys():
                sheet.cell(row, headings.index(column)+1, ",\n".join(farm_values[column])).alignment = Alignment(wrap_text=True, vertical='top')
            
            sheet.row_dimensions[row].height = None
            row+=1
        
        
    
    wb.save(output_file)
    
    
    

def filename_pattern_check(filename, row_num):
    ''' Checks whether the filename matches the expected format and extracts the components needed for further processing. If the filename does not match the expected pattern then ValueError exception is thrown.
    
    Keyword arguments:
        filename - string with the filename to be checked
        row_num - string with number of row in spreadsheet
        
    Outputs:
        Tuple containing the central part of the filename and the final count at the end of the filename   
    '''
    
    if m := re.match(r"MAF32-(\d*-\d*)( Pt\d*)?_(\d*).tif", filename):
        ref_component = m.group(1)
        iteration_num = m.group(3)
        return (ref_component, iteration_num)
    else:
        raise ValueError("Row " + row_num + ": " + filename + " does not match expected pattern. Further checks on filenames could not be carried out and an accurate reference could not be generated.")
         
# Group 1: Filenames 
# Input columns: A (filename_1) and B (filename_2). 
# Expecting two to five rows of data (depending on number of forms for that farm)
# Check 1: the format should be quite consistent: MAF32-\d*-\d*__\d*.tif
# Check 2: the filenames should all match up to the underscore
# Check 3: filename_1, filename_2 should consist of consecutive numbers in each row
# Return comma separated list of file names [Output column: A (Filenames)]
# Warnings if checks don't pass [Output column: B (File Warnings)]
# Warnings if unexpected number of rows matched
def filename_checks(filename1, filename2, row_num):
    ''' Carries out the required checks on the filenames for each row
    
        Keyword arguments:
            filename1 - string with name of first file
            filename2 - string with name of second file
            row_num - string with number of row in spreadsheet 
            
        Outputs:
            Tuple containing the central part of the filename for use in the reference and a list of warnings
    '''
    warnings = []
    
    # check one - match MAF32-\d*-\d*_\d*.tif
    
    try:
        ref_part1, iteration_num1 = filename_pattern_check(filename1, row_num)
    except ValueError as e:
        warnings.append(str(e))
        ref_part1 = ""
        iteration_num1 = -1
        print(iteration_num1 + ": " + iteration_num2)
        print(warnings) 
        
    try:
        ref_part2, iteration_num2 = filename_pattern_check(filename2, row_num)

        # check two - centre sections match
        if ref_part1 != ref_part2 and ref_part1 != "":
            warnings.append("Row " + row_num + ": Mismatch in the file names: " + filename1 + ", " + filename2)

        
        # check three - sequence
        if (int(iteration_num1) != int(iteration_num2) + 1) and (int(iteration_num1) != int(iteration_num2) - 1) and iteration_num1 > 0:
            warnings.append("Row " + row_num + ": File names are not consecutive")
        
        print(iteration_num1 + ": " + iteration_num2)
        print(warnings)    
        return (ref_part1, warnings)
    
    except ValueError as e:
        warnings.append(str(e))
        print(iteration_num1 + ": " + iteration_num2)
        print(warnings)   
        return ("0-0", warnings)
    
    

def extract_farms(full_csv):
    '''
    '''
    
    farms = {}
    
    for row_num, row in enumerate(full_csv, 2):
        file1 = row['filename_1']
        file2 = row['filename_2']
        ref_component, warnings = filename_checks(file1, file2, str(row_num))
                
        primary_farm_number = row['primary_farm_number']
        additional_farm_number = row['additional_farms']
        form = row['document_type']
        
        type_warning = []
        doc_check = doc_type_check(form)
        if len(doc_check) > 0:
            type_warning = ["Row " + str(row_num) + ": " + doc_check]
        
        form_values = {"Type": [form]}

        farm_refs, ref_warnings = generate_references(ref_component.replace("-","/"), primary_farm_number, additional_farm_number, str(row_num), farms.keys())
        
        for temp_ref in farm_refs.keys():
            core_ref = temp_ref.split("-")[0]
            if core_ref in farms.keys() and form not in farms[core_ref]["Type"]: 
                ref = core_ref           
                farms[ref]["Type"] += [form]          
            elif core_ref in farms.keys() and form in farms[core_ref]["Type"]:
                ref = temp_ref
                farms[ref] = {"Type": [form]}               
                ref_warnings.append("Row " + str(row_num) + ": Error - Duplicate reference/form")
            else:
                ref = core_ref 
                farms[ref] = form_values 
        
        if "Filenames" in farms[ref].keys():
            farms[ref]["Filenames"] += [file1, file2]  
        else:
            farms[ref]["Filenames"] = [file1, file2]
            
        if "Filename Warnings" in farms[ref].keys():
            farms[ref]["Filename Warnings"] += warnings
        else:
            farms[ref]["Filename Warnings"] = warnings
        
        if "Reference Warnings" in farms[ref].keys():
            farms[ref]["Reference Warnings"] += ref_warnings
        else:
            farms[ref]["Reference Warnings"] = ref_warnings

        if "Type Warnings" in farms[ref].keys():
            farms[ref]["Type Warnings"] += type_warning
        else:
            farms[ref]["Type Warnings"] = type_warning
                
    return (farms)  

    


# Group 0: Reference
# Input columns: A/B (filenames), F (primary_farm_number), G (additional_farms)
# return "MAF 32 " + box number (string after first hyphen and before underscore, replace hyphens with slashed in columns A and B in source which should match) + "/" + farm number (F or G in source) [Output column: U (Reference)] 
# Warnings: if generated using column G [Output column: V (Reference Warnings)] 
def generate_references(box_string, primary_farm_string, additional_farm_string, row_num, existing_refs):
    ''' Create a reference string for each farm
    
        Keyword arguments:
            box_string - string with the box component of the reference
            primary_farm_string - string with number for primary farm
            additional_farm_string - semi-colon separated list of additional farm numbers
            row_num - string with number of row in spreadsheet
            existing_ref - list of existing references 
            
        Outputs:
            Tuple containing a list of generated references and a list of warnings
    '''
    ref_list = {}
    warnings = []
    
    if primary_farm_string != "" and additional_farm_string == "":
        ref = generate_ref("MAF 32/" + box_string + "/" + primary_farm_string, existing_refs)           
        ref_list[ref] = "Primary"
       
    elif primary_farm_string == "" and additional_farm_string != "":
        for additional_farm in additional_farm_string.split(";"):
            ref = generate_ref("MAF 32/" + box_string + "/" + additional_farm, existing_refs)           
            ref_list[ref] = "Additional"
        warnings.append("Row " + row_num + ": Error - Additional farm but no primary farm given")
        
    elif primary_farm_string != "" and additional_farm_string != "":
        ref = generate_ref("MAF 32/" + box_string + "/" + primary_farm_string, existing_refs)           
        ref_list[ref] = "Primary"
        
        for additional_farm in additional_farm_string.split(";"):
            ref = generate_ref("MAF 32/" + box_string + "/" + additional_farm, existing_refs)           
            ref_list[ref] = "Additional"          
               
        warnings.append("Row " + row_num + ": Additional farms present")
    else:
        warnings.append("Row " + row_num + ": Error - No farm number specified")
        
    return (ref_list, warnings)  

def generate_ref(base_ref, existing_refs):
    ''' Check whether the reference already exists and return it or an alternate reference so that the reference is unique
    
        keyword arguments: 
            base_ref - string with the proposed reference 
            existing_refs - list of already used references
        
        outputs:
            Reference string      
    '''
    
    if base_ref in existing_refs:
        counter = 1
        temp_ref = base_ref
        while temp_ref in existing_refs:
            temp_ref = temp_ref.split("-")[0] + "-" + str(counter)
            counter += 1   
         
        return temp_ref
    else:
        return base_ref



# Group 2: Type of documents
# Input column: C (document_type)
# Expecting two to five rows of data (depending on number of forms for that farm)
# Check 1: allowed values are: "C 51/SSY form", "B 496/EI form", "C 47/SSY form", "C 49/SSY form", "SF form C 69/SSY", "other"
# Return comma separated list of forms [Output column: C (Type)]
# Warnings if content doesn't match allowed values [Output column: D (Type Warnings)]
# Warnings if unexpected number of rows matched

def doc_type_check(type):
    allowed_types = ["C 51/SSY form", "B 496/EI form", "C 47/SSY form", "C 49/SSY form", "SF form C 69/SSY", "other"]
    if type in allowed_types:
        return ""
    else:
        return "Unknown document type."

# Group 3: Farm number
# Input column: D (county), E (parish), F (primary_farm_number) and G (additional_farms - semi-colon separated list) in source spreadsheet
# Expecting three rows of data
# Check 1: lettercode/parish number/farm number they should all match
# Return farm number  [Output column: E (Farm Number)]
# Return additional farm number(s) on separate row(s) and fill in the rest of values from the form that mentions the additional farm(s)
# Warning: generate a warning if not match [Output column: F (Farm Warnings)]
# Warning: flag any case in which column G is filled [Output column: F (Farm Warnings)]
# Warnings if unexpected number of rows matched

# Group 4: Farm
# Input column: H (farm_name)
# Expecting 2 rows of data
# Check 1: values should be similar, ignoring asterisk and blanks. Return combined value.
# Return combined value [Output column: G (Farm Name)]  
# Warning: if not similar [Output column: H (Farm Name Warnings)]
# Warnings if unexpected number of rows matched   

# Group 5: Landowner
# Input columns: M (owner_title), N (owner_individual_name), O (owner_group_names - semi-colon separated list), P (owner_address - semi-colon separated list)
# Expecting 1 row of data (Column C: "B 496/EI form")
# Return combined values [Output column: I (Landowner)]  
#       M and N are to be merged, if both are given. 
#       If N contains asterisk, data from O should be taken
#       P is the address. 
#       O and P should be matched on position in list
# Check 1: same number of tokens in column O (owner group names) and column P (owner addresses) in semi-colon separated lists
# Warning: if N and O both have data [Output column: J (Landowner Warnings)] 
# Warning: if M and O both have data [Output column: J (Landowner Warnings)] 
# Warning: if mismatch with number of owner group names and owner addresses
# Warnings if unexpected number of rows matched

# Group 6: Farmer
# Input columns: I (addressee_title), J (addressee_individual_name), K (addressee_group_names), L (address) 
# Input columns: Q (farmer_title), R (farmer_individual_name), S (farmer_group_names), T (farmer_address)
# Check 1: column I and column Q are similar (individual name titles)
# Check 2: column J and column R are similar (individual name)
# Check 3: column K and column S are similar  (group names)
# Check 4: column T and column L are similar  (addresses)
# Return combined values (name, address) of either I/Q/J/R or K/S and L/T [Output column: I (Farmer)]  
# Warnings: if I/Q/J/R and K/S both given [Output column: I (Farmer Warnings)]  
# Warnings: if not similar [Output column: I (Farmer Warnings)] 

# Group 7: Acreage
# Input column: U (acreage)
# Expecting 1 row of data
# Return value [Output column: M (Acreage)] 

# Group 8: OS
# Input column: V (OS_map_sheet)
# Excepting 1 row of data
# Return value [Output column: O (OS Sheet)] 

# Group 9: Field Date
# Input column: W (field_info_date)
# Expecting 1 row of data
# Check if valid date
# Return value [Output column: Q (Field Date)] 
# Warnings: if not valid date [Output column: R (Field Date Warnings)] 
# Warnings: if date is not earlier or equal to Primary Date [Output column: R (Field Date Warnings)] 
# Warnings: if unexpected number of rows matched

# Group 9: Primary Date
# Input column: X (primary_record_date - semi-colon separated)
# Expecting 1 row of data
# Check if valid date
# Return value as comma separated list if more then one date [Output column: S (Primary Date)] 
# Warnings: if not valid date
# Warnings: if date is not later or equal to Field Date [Output column: T (Primary Date Warnings)] 
# Warnings: if unexpected number of rows matched




processing_folder = "processing"
load_spreadsheet_data(processing_folder)