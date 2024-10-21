# Create a QA spreadsheet
# 
# Input Columns: filename_1, filename_2, document_type, county, parish, primary_farm_number, additional_farms, farm_name, addressee_title, addressee_individual_name, addressee_group_names, address, owner_title, owner_individual_name, owner_group_names, owner_address, farmer_title, farmer_individual_name, farmer_group_names, farmer_address, acreage, OS_map_sheet, field_info_date, primary_record_date
#    
# Output Columns: Expected Ref, Ref Warnings, Filenames, File Warnings, Type, Type Warnings, Farm Number, Farm Warnings, Farm Name, Farm Name Warnings, Landowner, Landowner Warnings, Farmer, Farmer Warnings, Acreage, OS Sheet Num, OS Warnings, Field Date, Field Date Warnings, Primary Date, Primary Date Warnings
#

# Need to match rows on filenames (before underscore) + farm number

import csv, re
from pathlib import Path

def load_spreadsheet_data(processing_folder):
    ''' Process any files in the processing folder
    '''
    try: 
        for file in Path(processing_folder).glob("*.csv"):        
            with open(file, newline='') as f:
                values = csv.DictReader(f) 
                farms = extract_farms(values)  
                print(farms)
                
    except OSError as e:
        print("Error in data loading: " + e)

def filename_pattern_check(filename):
    '''
    '''
    
    if m := re.match("MAF32-(\d*-\d*)_(\d*).tif", filename):
        ref_component = m.group(1)
        iteration_num = m.group(2)
        return ((ref_component, iteration_num), "")
    else:
        return (("", ""), filename + " does not match expected pattern") 
         

def filename_checks(filename1, filename2):
    '''
    '''
    warnings = []
    
    # check one - match MAF32-\d*-\d*_\d*.tif
    
    components, warning = filename_pattern_check(filename1)
    
    if len(warning) > 0:
        warnings.append(warning)
        
    ref_part, iteration_num1 = components
    ref_component = {ref_part}
    
    components, warning = filename_pattern_check(filename2)
    
    if len(warning) > 0:
        warnings.append(warning)
        
    ref_part, iteration_num2 = components
    ref_component.add(ref_part)

    # check two - centre sections match
    
    if len(ref_component) != 1:
        warnings.append("Mismatch in the file names")
    
    # check three - sequence
    if (iteration_num1 != iteration_num2 + 1) and (iteration_num1 != iteration_num2 - 1):
        warnings.append("File names are not consecutive")
    
    return (ref_component, warnings)
    
    

def extract_farms(full_csv):
    '''
    '''
    
    for row in full_csv:
        ref_component, warnings = filename_checks(row['filename1'], row['filename2'])
        print(ref_component)
        print(warnings)
    

    

    


# Group 0: Reference
# Input columns: A/B (filenames), F (primary_farm_number), G (additional_farms)
# return "MAF 32 " + box number (string after first hyphen and before underscore, replace hyphens with slashed in columns A and B in source which should match) + "/" + farm number (F or G in source) [Output column: U (Reference)] 
# Warnings: if generated using column G [Output column: V (Reference Warnings)] 
def generate_references():
    '''
    '''
    references = {}
    
    return references
    
    

# Group 1: Filenames 
# Input columns: A (filename_1) and B (filename_2). 
# Expecting two to five rows of data (depending on number of forms for that farm)
# Check 1: the format should be quite consistent: MAF32-\d*-\d*__\d*.tif
# Check 2: the filenames should all match up to the underscore
# Check 3: filename_1, filename_2 should consist of consecutive numbers in each row
# Return comma separated list of file names [Output column: A (Filenames)]
# Warnings if checks don't pass [Output column: B (File Warnings)]
# Warnings if unexpected number of rows matched

# Group 2: Type of documents
# Input column: C (document_type)
# Expecting two to five rows of data (depending on number of forms for that farm)
# Check 1: allowed values are: "C 51/SSY form", "B 496/EI form", "C 47/SSY form", "C 49/SSY form", "SF form C 69/SSY", "other"
# Return comma separated list of forms [Output column: C (Type)]
# Warnings if content doesn't match allowed values [Output column: D (Type Warnings)]
# Warnings if unexpected number of rows matched

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
# Check 1: column I and column Q (titles)
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
