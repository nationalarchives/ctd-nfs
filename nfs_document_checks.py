# Create a QA spreadsheet
# 
# Input Columns: filename_1, filename_2, document_type, county, parish, primary_farm_number, additional_farms, farm_name, addressee_title, addressee_individual_name, addressee_group_names, address, owner_title, owner_individual_name, owner_group_names, owner_address, farmer_title, farmer_individual_name, farmer_group_names, farmer_address, acreage, OS_map_sheet, field_info_date, primary_record_date
#    
# Output Columns: Expected Ref, Ref Warnings, Filenames, File Warnings, Type, Type Warnings, Farm Number, Farm Warnings, Farm Name, Farm Name Warnings, Landowner, Landowner Warnings, Farmer, Farmer Warnings, Acreage, OS Sheet Num, OS Warnings, Field Date, Field Date Warnings, Primary Date, Primary Date Warnings
#
# Need to match rows on filenames (before underscore) + farm number

# Functions:
#   load_spreadsheet_data(processing_folder)
#   output_excel(output_file, values)
#   filename_pattern_check(filename, row_num)
#   reference_pattern_check(ref, row_num)
#   filename_checks(filename1, filename2, row_num)
#   doc_type_check(type, row_num)
#   extract_farms(full_csv)
#   generate_references(box_string, primary_farm_string, additional_farm_string, row_num, existing_refs)
#   generate_ref(base_ref, existing_refs)
#   generate_farm_number_for_record(county, parish, farm_nums, ref)
#   generate_farm_numbers(county, parish, farm_nums)
#   get_combined_farm_names_by_ref(farm_names)
#   get_combined_owner_details_by_ref(owner_details)
#   get_combined_farmer_details_by_ref(farmer_details, addressee_details)
#   get_combined_details_by_ref(details, expected_count = -1)
#   array_zip(details_array, key = "")
#   dic_merge(dic1, dic2)
#   date_processing(field_date, primary_dates, row_num)
#   date_check(potential_date, row_num)


#####################
#   To Do
#


import csv, re, datetime
import data_normalisation as dn
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
#from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from rapidfuzz import fuzz

def load_spreadsheet_data(processing_folder):
    ''' Process any csv files in the processing folder

        Keyword Arguments:
            processing_folder - string with path to folder
    '''
    
    try: 
        for file in Path(processing_folder).glob("*.csv"):     
  
            base_filename = Path(file).stem
            print("Processing file:" + str(base_filename))   
                        
            with open(file, newline='') as f:
                values = csv.DictReader(f) 
                farm_values = extract_farms(values)  
                #print(farm_values)                
            
            #print(file)    
            output_excel(Path(processing_folder, "output", base_filename + ".xlsx"), farm_values)
                
    except OSError as e:
        print("Error in data loading: " + e)
        

def output_excel(output_file, values):
    ''' Save a spreadsheet containing the values for checking
    
        keyword Arguments:
            output_file - path to output file
            values - nested dictionary of values to be output. The top keys are the unique reference for each farm and nested below that are the values for that farm with the column name as the keys
            
        Outputs:
            No return but a file is saved to the specified folder
    '''
    
    wb = Workbook()
    sheet = wb.active
    
    headings = ["Reference", "Reference Warnings", "Filenames", "Filename Warnings", "Type", "Type Warnings", "Farm Number", "Farm Number Warnings", "Farm Name", "Farm Name Warnings", "Landowner", "Landowner Warnings", "Farmer", "Farmer Warnings", "Acreage", "Acreage Warnings", "OS Sheet Number", "Field Date", "Field Date Warnings", "Primary Date", "Primary Date Warnings"]
    default_widths = [20, 20, 30, 20, 15, 20, 15, 20, 30, 20, 30, 20, 30, 20,15, 20, 15, 15, 20, 15, 20]
 
    for i in range(0, len(headings)):
        column = headings[i]
        col_num = i+1
        
        sheet.cell(1, col_num, column).font = Font(bold=True)
        sheet.column_dimensions[get_column_letter(col_num)].width = default_widths[i]  
        
        row = 2
        for ref in values:
            sheet.cell(row, 1, ref)
            
            farm_values = values[ref]
            #print(ref + ": " + ", ".join(farm_values))

            if column != "Reference" and column in farm_values.keys():
                sheet.cell(row, headings.index(column)+1, ",\n".join(farm_values[column])).alignment = Alignment(wrap_text=True, vertical='top')
            
            sheet.row_dimensions[row].height = None
            row+=1
               
    print("Saving " + str(output_file))
    wb.save(output_file)
        

def filename_pattern_check(filename, row_num):
    ''' Checks whether the filename matches the expected format and extracts the components needed for further processing. If the filename does not match the expected pattern then ValueError exception is thrown.
    
    Keyword Arguments:
        filename - string with the filename to be checked
        row_num - string with number of row in spreadsheet
        
    Outputs:
        Tuple containing the central part of the filename and the final count at the end of the filename or raises an ValueError  
    '''
    
    if filename != "":
        if m := re.match(r"MAF32-(\d*-\d*)( Pt\d*)?_(\d*).tif", filename):
            ref_component = m.group(1)
            iteration_num = m.group(3)
            return (ref_component, iteration_num)
        else:
            raise ValueError("Row " + row_num + ": " + filename + " does not match expected pattern. Further checks on filenames could not be carried out and an accurate reference could not be generated.")
    else:
        raise ValueError("Row " + row_num + ": Error - Blank filename found. Further checks on the filename could not be carried out and an accurate reference could not be generated.")        


def reference_pattern_check(ref, row_num):
    ''' Checks whether the reference identifier matches the expected pattern
 
    Keyword Arguments:
        filename - string with the filename to be checked
        row_num - string with number of row in spreadsheet
        
    Outputs:   
        The reference value or raises a ValueError   
    '''
    
    if ref != "":
        if re.match(r"^MAF 32/\d*/\d*/\d*$", ref):
            #print(ref + " matches pattern.")
            return (ref)
        else:
            #print(ref + " not match pattern.")
            raise ValueError("Row " + row_num + ": " + ref + " does not match expected pattern. Further work with this reference may contain inaccuracies.")
    else:
        raise ValueError("Row " + row_num + ": Error - Blank reference found. Further work with this reference could not be carried out and farm information could not be generated.")        
        
         
# Group 1: Filenames 
# Input columns: A (filename_1) and B (filename_2). 
# Expecting two to five rows of data (depending on number of forms for that farm) - TO DO
# Check 1: the format should be quite consistent: MAF32-\d*-\d*__\d*.tif
# Check 2: the filenames should all match up to the underscore
# Check 3: filename_1, filename_2 should consist of consecutive numbers in each row
# Return comma separated list of file names [Output column: A (Filenames)]
# Warnings if checks don't pass [Output column: B (File Warnings)]
# Warnings if unexpected number of rows matched
def filename_checks(filename1, filename2, row_num):
    ''' Carries out the required checks on the filenames for each row
    
        Keyword Arguments:
            filename1 - string with name of first file
            filename2 - string with name of second file
            row_num - string with number of row in spreadsheet 
            
        Outputs:
            Tuple containing the central part of the filename for use in the reference and a set of warnings
    '''
    warnings = set()
    
    # check one - match MAF32-\d*-\d*_\d*.tif
    
    if not(filename1 == "" and filename2 == ""):   
        try:
            ref_part1, iteration_num1 = filename_pattern_check(filename1, row_num)
        except ValueError as e:
            warnings.add(str(e))
            ref_part1 = ""
            iteration_num1 = -1
            #print(iteration_num1 + ": " + iteration_num2)
            #print(warnings) 
        
        try:
            ref_part2, iteration_num2 = filename_pattern_check(filename2, row_num)

            # check two - centre sections match
            if ref_part1 != ref_part2 and ref_part1 != "":
                warnings.add("Row " + row_num + ": Mismatch in the file names: " + filename1 + ", " + filename2)
            
            # check three - sequence
            if (int(iteration_num1) != int(iteration_num2) + 1) and (int(iteration_num1) != int(iteration_num2) - 1) and int(iteration_num1) > 0:
                warnings.add("Row " + row_num + ": File names (" + iteration_num1 + " and " + iteration_num2 + ") are not consecutive")
            
            if ref_part1 == "" or ref_part2 == "":
                warnings.add("Row " + row_num + ": Only on File name given (" + iteration_num1 + iteration_num2 + ")")

            #print(iteration_num1 + ": " + iteration_num2)
            #print(warnings)  
                
            if ref_part1 != "":
                return (ref_part1, warnings)
            else:
                return (ref_part2, warnings)            
        
        except ValueError as e:
            warnings.add(str(e))
            return ("0-0", warnings)
    else:
        warnings.add("Row " + row_num + ": Error - File names missing")
        return ("0-0", warnings)
        
    
# Group 2: Type of documents
# Input column: C (document_type)
# Expecting two to five rows of data (depending on number of forms for that farm)
# Check 1: allowed values are: "C 51/SSY form", "B 496/EI form", "C 47/SSY form", "C 49/SSY form", "SF form C 69/SSY", "other"
# Return comma separated list of forms [Output column: C (Type)]
# Warnings if content doesn't match allowed values [Output column: D (Type Warnings)]
# Warnings if unexpected number of rows matched

def doc_type_check(type, row_num):
    ''' Checks if the type of document matches one of the valid types
    
        Keyword Arguments:
            type - string with document type 
            row_num - string with number of row in spreadsheet        
             
        Outputs: 
            Type value as string or raises a ValueError
    '''
    
    allowed_types = ["C 51/SSY form", "B 496/EI form", "C 47/SSY form", "C 49/SSY form", "SF form C 69/SSY", "Other"]
        
    if type in allowed_types:
        return type
    else:
        raise ValueError("Row " + row_num + ": Unknown document type (" + type + ") found.")
    

def extract_farms(full_csv):
    ''' 
        Keyword Arguments:
            full_csv - dictionary with the values from the CSV and the column headings as keys
    
        Outputs:
            Farm values and warnings in a nested dictionary using the farm reference as a keys and the output column names as the second level keys
    '''
    
    farms = {}
    row_counts = {}
    raw_farm_info = {}    
    
    for row_num, row in enumerate(full_csv, 2):
        file1 = row['filename_1']
        file2 = row['filename_2']
        ref_component, filename_warnings = filename_checks(file1.strip(), file2.strip(), str(row_num))
                
        primary_farm_number = row['primary_farm_number']
        additional_farm_number = row['additional_farms']
        form = row['document_type']
        form = form.strip()
        
        type_warnings = set()
        try:
            doc_type_check(form, str(row_num))
        except ValueError as ve:
            type_warnings.update([str(ve)])

        farm_refs, ref_warnings = generate_references(ref_component.replace("-","/"), primary_farm_number.strip(), additional_farm_number.strip(), str(row_num), farms.keys())
        
        #print(farm_refs)
        #print(ref_warnings)

        for temp_ref in farm_refs.keys():
            #core_ref = temp_ref.split("-")[0]
            ref = temp_ref.split("-")[0]
            #print("Checking: " + core_ref + ": " + form)
            if ref in farms.keys() and form not in farms[ref]["Type"]: 
                #ref = core_ref            
                farms[ref]["Type"] += [form]
                #print("Row " + str(row_num) +  ": Core ref in dict, form not in dict. Adding " + form + " to " + ref)       
            elif ref in farms.keys() and form in farms[ref]["Type"]:
                #ref = temp_ref
                #print("Row " + str(row_num) + ": Core ref (" + ref + ") in dict and form in dict")
                if ref in farms.keys():
                    farms[ref]["Type"] += [form]
                else:
                    farms[ref] = {"Type": [form]}  
                                 
                ref_warnings.add("Row " + str(row_num) + ": Warning - Multiple '" + form + "' forms for " + ref)
            else:
                #ref = core_ref 
                farms[ref] = {"Type": [form]}
                if ref not in raw_farm_info.keys():
                    raw_farm_info[ref] = dict()
                #print("Row " + str(row_num) + ": Neither Core ref or form in dict. Adding " + form + " to " + ref)

            # count rows
            if ref in row_counts.keys():
                row_counts[ref]["Total"] += 1
            else:
                row_counts[ref] = {"Total":1, "Row": row_num}
        
            # generate farm number    
            county = row['county']
            parish = row['parish']
                           
            if farm_refs[temp_ref] == "Primary":
                farm_numbers = row['primary_farm_number']     
            else:
                farm_numbers = row['additional_farms']
            
            farm_nums = generate_farm_number_for_record(county, parish, farm_numbers, ref)

            if "Farm number" in farms[ref].keys():
                farms[ref]["Farm Number"].update(farm_nums)
                if len(farm_nums) == 1:
                    row_counts[ref]["Farm Number"] += 1
            else:
                farms[ref]["Farm Number"] = farm_nums
                if len(farm_nums) == 1:
                    row_counts[ref].update({"Farm Number":1})

            
            # Type counts            
            if "Type" in row_counts[ref].keys() and form != "":
                row_counts[ref]["Type"] += 1
            elif form != "":
                row_counts[ref].update({"Type":1})                       
        
            # Filenames
            if "Filenames" in farms[ref].keys():
                if file1 != "" and file2 != "":
                    farms[ref]["Filenames"].update({file1, file2})  
                    row_counts[ref]["Filenames"] += 1
                elif file1 != "":
                    farms[ref]["Filenames"].update({file1})  
                else:
                    farms[ref]["Filenames"].update({file2})  
            else:                
                if file1 != "" and file2 != "":
                    farms[ref]["Filenames"] = {file1, file2} 
                    row_counts[ref].update({"Filenames":1})
                elif file1 != "":
                    farms[ref]["Filenames"] = {file1}
                    row_counts[ref].update({"Filenames":0}) 
                else:
                    farms[ref]["Filenames"] = {file2}
                    row_counts[ref].update({"Filenames":0}) 
                
            if "Filename Warnings" in farms[ref].keys():
                farms[ref]["Filename Warnings"].update(filename_warnings)
            else:
                farms[ref]["Filename Warnings"] = filename_warnings
                
            # H (farm_name)
            farm_name = row['farm_name']
            if farm_name != "" and farm_name != "*":
                if "Farm Name" in raw_farm_info[ref].keys():
                    raw_farm_info[ref]["Farm Name"] += [farm_name]

                else:
                    raw_farm_info[ref].update({"Farm Name": [farm_name]})

            
            # M (owner_title), N (owner_individual_name), O (owner_group_names - semi-colon separated list), P (owner_address - semi-colon separated list)
            owner_title = row['owner_title']
            owner_individual_name = row['owner_individual_name']
            owner_group_names = row['owner_group_names']
            owner_addresses = row['owner_address']
            
            combined = owner_title + owner_individual_name + owner_group_names + owner_addresses
            combined = combined.replace("*", "")
            
            # If N/'individual name' contains asterisk, data from O/'group names) should be taken
            
            if len(combined) > 0:
                if "Landowner" in raw_farm_info[ref].keys():
                    raw_farm_info[ref]["Landowner"]["Title"] += [owner_title]
                    raw_farm_info[ref]["Landowner"]["Individual Name"] += [owner_individual_name]
                    raw_farm_info[ref]["Landowner"]["Group Names"] += [owner_group_names.split(";")]
                    raw_farm_info[ref]["Landowner"]["Addresses"] += [owner_addresses.split(";")]
                    
                else:
                    raw_farm_info[ref].update({"Landowner": {"Title": [owner_title]}})
                    raw_farm_info[ref]["Landowner"].update({"Individual Name": [owner_individual_name]})
                    raw_farm_info[ref]["Landowner"].update({"Group Names": [owner_group_names.split(";")]})
                    raw_farm_info[ref]["Landowner"].update({"Addresses": [owner_addresses.split(";")]}) 
                    
                #print(raw_farm_info[ref]["Landowner"])                                

            # Input columns: I (addressee_title), J (addressee_individual_name), K (addressee_group_names), L (address) 
            # Input columns: Q (farmer_title), R (farmer_individual_name), S (farmer_group_names), T (farmer_address)
            addressee_title = row['addressee_title']
            addressee_individual_name = row['addressee_individual_name']
            addressee_group_names = row['addressee_group_names']
            addresses = row['address']
            farmer_title = row['farmer_title']
            farmer_individual_name = row['farmer_individual_name']
            farmer_group_names = row['farmer_group_names']
            farmer_addresses = row['farmer_address']
            
            combined = addressee_title + addressee_individual_name + addressee_group_names + addresses + farmer_title + farmer_individual_name + farmer_group_names + farmer_addresses
            combined = combined.replace("*", "")
            
            #print(ref)
            
            if len(combined) > 0:            
                if "Farmer" in raw_farm_info[ref].keys():
                    raw_farm_info[ref]["Farmer"]["Title"] += [farmer_title]
                    raw_farm_info[ref]["Farmer"]["Individual Name"] += [farmer_individual_name]
                    raw_farm_info[ref]["Farmer"]["Group Names"] += [farmer_group_names.split(";")]
                    raw_farm_info[ref]["Farmer"]["Addresses"] += [farmer_addresses.split(";")] 
                    raw_farm_info[ref]["Addressee"]["Title"] += [addressee_title]
                    raw_farm_info[ref]["Addressee"]["Individual Name"] += [addressee_individual_name]
                    raw_farm_info[ref]["Addressee"]["Group Names"] += [addressee_group_names.split(";")]
                    raw_farm_info[ref]["Addressee"]["Addresses"] += [addresses.split(";")]                                     
                else:
                    raw_farm_info[ref].update({"Farmer": {"Title": [farmer_title]}})
                    raw_farm_info[ref]["Farmer"].update({"Individual Name": [farmer_individual_name]})
                    raw_farm_info[ref]["Farmer"].update({"Group Names": [farmer_group_names.split(";")]})
                    raw_farm_info[ref]["Farmer"].update({"Addresses": [farmer_addresses.split(";")]}) 
                    raw_farm_info[ref].update({"Addressee": {"Title": [addressee_title]}})
                    raw_farm_info[ref]["Addressee"].update({"Individual Name": [addressee_individual_name]})
                    raw_farm_info[ref]["Addressee"].update({"Group Names": [addressee_group_names.split(";")]})
                    raw_farm_info[ref]["Addressee"].update({"Addresses": [addresses.split(";")]})                  
            
            # Group 7: Acreage
            # Input column: U (acreage - semi-colon separated list)
            # Expecting 1 row of data
            # Return value [Output column: M (Acreage)]
            # Warning if multiple values     
            acreage = row['acreage']
            if acreage != "":
                if "Acreage" in farms[ref].keys():
                    farms[ref]["Acreage"].update({acreage})
                else:
                    farms[ref].update({"Acreage": {acreage}})
                    
                
                if "Acreage" in row_counts[ref].keys():
                    row_counts[ref]["Acreage"] += 1
                else:
                    row_counts[ref].update({"Acreage":1}) 

                        
            # Group 8: OS
            # Input column: V (OS_map_sheet)
            # Excepting 1 row of data
            # Return value [Output column: O (OS Sheet)]             
            OS_map = row['OS_map_sheet']
            if OS_map != "":
                if "OS Sheet Number" in farms[ref].keys():
                    farms[ref]["OS Sheet Number"].update(OS_map)
                    row_counts[ref]["OS_sheet_number"] += 1
                else:
                    farms[ref].update({"OS Sheet Number": {OS_map}})
                    row_counts[ref].update({"OS_sheet_number":1}) 

            # Dates
            field_date = row["field_info_date"]
            primary_date = row["primary_record_date"]
            
            field_date_values, primary_date_values = date_processing(field_date, primary_date, str(row_num))
            checked_field_date, field_date_warnings = field_date_values
            checked_primary_date, primary_date_warnings = primary_date_values
            
            #print("Checked Field Date: " + checked_field_date)
            #print("Checked Primary Date: " + checked_primary_date)
            
            if checked_field_date != "":
                if "Field Date" in farms[ref].keys():               
                    farms[ref]["Field Date"].add(checked_field_date)
                    row_counts[ref]["Field Date"] += 1
                else:
                    farms[ref].update({"Field Date": {checked_field_date}})
                    row_counts[ref].update({"Field Date":1})
            
            if checked_primary_date != "":            
                if "Primary Date" in farms[ref].keys():                
                    farms[ref]["Primary Date"].add(checked_primary_date)
                    row_counts[ref]["Primary Date"] += 1
                else:
                    farms[ref].update({"Primary Date": {checked_primary_date}})
                    row_counts[ref].update({"Primary Date":1})            
            

            try:
                reference_pattern_check(ref, str(row_num))
            except ValueError as ve:
                if "Reference Warnings" in farms[ref].keys():
                    farms[ref]["Reference Warnings"] = {str(ve)}   
 
                                
            # Warnings
            if "Reference Warnings" in farms[ref].keys():
                farms[ref]["Reference Warnings"].update(ref_warnings)
            else:
                farms[ref]["Reference Warnings"] = ref_warnings
                
            #print(farms[ref]["Reference Warnings"])

            if "Type Warnings" in farms[ref].keys():
                farms[ref]["Type Warnings"].update(type_warnings)
            else:
                farms[ref]["Type Warnings"] = type_warnings
            
            farm_num_warning = {"Row " + str(row_num) + ": Error in generated farm number - lettercode/parish number/farm number mismatch"}    
            if "Farm Number Warnings" in farms[ref].keys() and len(farm_nums) > 1:
                farms[ref]["Farm Number Warnings"].update(farm_num_warning)
            elif len(farm_nums) > 1:
                farms[ref]["Farm Number Warnings"] = farm_num_warning
            else:
                farms[ref]["Farm Number Warnings"] = set()

            acreage_warning = {"Row " + str(row_num) + ": multiple acreage given"}    
            if "Acreage Warnings" in farms[ref].keys() and ";" in acreage:
                farms[ref]["Acreage Warnings"].update(acreage_warning)
            elif ";" in acreage:
                farms[ref]["Acreage Warnings"] = acreage_warning
            else:
                farms[ref]["Acreage Warnings"] = set()

            if "Field Date Warnings" in farms[ref].keys():
                farms[ref]["Field Date Warnings"].update(field_date_warnings)
            else:
                farms[ref]["Field Date Warnings"] = field_date_warnings

            if "Primary Date Warnings" in farms[ref].keys():
                farms[ref]["Primary Date Warnings"].update(primary_date_warnings)
            else:
                farms[ref]["Primary Date Warnings"] = primary_date_warnings

    #print(raw_farm_info) 
    # Farm names
    farm_names = {}
    for farm_ref, farm_data in raw_farm_info.items():
        if "Farm Name" in farm_data.keys():
            farm_names[farm_ref] = farm_data["Farm Name"]
          
    combined_farm_names, combined_farm_name_warnings = get_combined_farm_names_by_ref(farm_names)
    #print(combined_farm_names)
    
    for ref, combined_farm_name in combined_farm_names.items():
        farms[ref].update({"Farm Name": [combined_farm_name]})
        farms[ref].update({"Farm Name Warnings": combined_farm_name_warnings[ref]})
    
    # Owner names
    owner_details = {}
    for owner_ref, owner_data in raw_farm_info.items():
        if "Landowner" in owner_data.keys():
            owner_details[owner_ref] = owner_data["Landowner"]    
    
    #print(owner_details)
    combined_owner_info, combined_owner_info_warnings = get_combined_owner_details_by_ref(owner_details) 

    for ref, combined_owner_info in combined_owner_info.items():
        farms[ref].update({"Landowner": [combined_owner_info]})
        farms[ref].update({"Landowner Warnings": combined_owner_info_warnings[ref]})    
 
    # Farmer names
    farmer_details = {}
    for farmer_ref, farmer_data in raw_farm_info.items():
        if "Farmer" in farmer_data.keys():
            farmer_details[farmer_ref] = farmer_data["Farmer"]   

    # Addressee names
    addressee_details = {}
    for addressee_ref, addressee_data in raw_farm_info.items():
        if "Addressee" in addressee_data.keys():
            addressee_details[addressee_ref] = addressee_data["Addressee"] 
    #print(farmer_details)
    #print(addressee_details)
    combined_farmer_info, combined_farmer_info_warnings = get_combined_farmer_details_by_ref(farmer_details, addressee_details)
    
    for ref, combined_farmer_info in combined_farmer_info.items():
        farms[ref].update({"Farmer": [combined_farmer_info]})
        farms[ref].update({"Farmer Warnings": combined_farmer_info_warnings[ref]})   
           
    #print(farms)   
    #print(row_counts)
                
    return (farms)  

    
# Group 0: Reference
# Input columns: A/B (filenames), F (primary_farm_number), G (additional_farms)
# return "MAF 32 " + box number (string after first hyphen and before underscore, replace hyphens with slashed in columns A and B in source which should match) + "/" + farm number (F or G in source) [Output column: U (Reference)] 
# Warnings: if generated using column G [Output column: V (Reference Warnings)] 
def generate_references(box_string, primary_farm_string, additional_farm_string, row_num, existing_refs):
    ''' Creates a reference string for each farm in the required format: "MAF 32 " + box number (with slashes) + "/" + farm number
    
        Keyword Arguments:
            box_string - string with the box component of the reference
            primary_farm_string - string with number for primary farm
            additional_farm_string - semi-colon separated list of additional farm numbers
            row_num - string with number of row in spreadsheet
            existing_ref - list of existing references 
            
        Outputs:
            Tuple containing a list of generated references and a list of warnings
    '''
    
    ref_list = {}
    warnings = set()
    
    if primary_farm_string != "" and additional_farm_string == "":
        ref = generate_ref("MAF 32/" + box_string + "/" + primary_farm_string, existing_refs)           
        ref_list[ref] = "Primary"
       
    elif primary_farm_string == "" and additional_farm_string != "":
        for additional_farm in additional_farm_string.split(";"):
            ref = generate_ref("MAF 32/" + box_string + "/" + additional_farm.strip(), existing_refs)           
            ref_list[ref] = "Additional"
        warnings.add("Row " + row_num + ": Error - Additional farm but no primary farm given")
        
    elif primary_farm_string != "" and additional_farm_string != "":
        ref = generate_ref("MAF 32/" + box_string + "/" + primary_farm_string, existing_refs)           
        ref_list[ref] = "Primary"
        
        for additional_farm in additional_farm_string.split(";"):
            ref = generate_ref("MAF 32/" + box_string + "/" + additional_farm.strip(), existing_refs)           
            ref_list[ref] = "Additional"          
               
        warnings.add("Row " + row_num + ": Warning - Additional farms present")
    else:
        warnings.add("Row " + row_num + ": Error - No farm number specified")
               
    return (ref_list, warnings)  


def generate_ref(base_ref, existing_refs):
    ''' Check whether the reference already exists and return it or an alternate reference so that the reference is unique
    
        Keyword Arguments: 
            base_ref - string with the proposed reference 
            existing_refs - list of already used references
        
        Outputs:
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


# Group 3: Farm number
# Input column: D (county), E (parish), F (primary_farm_number) and G (additional_farms - semi-colon separated list) in source spreadsheet
# Expecting three rows of data
# Check 1: lettercode/parish number/farm number they should all match
# Return farm number  [Output column: E (Farm Number)]
# Return additional farm number(s) on separate row(s) and fill in the rest of values from the form that mentions the additional farm(s)
# Warning: generate a warning if not match [Output column: F (Farm Warnings)]
# Warning: flag any case in which column G is filled [Output column: F (Farm Warnings)]
# Warnings if unexpected number of rows matched

def generate_farm_number_for_record(county, parish, farm_nums, ref):
    ''' Generates a unique farm number from the county code, parish code and farm number for a given reference
    
        Keyword Arguments:
            county - string with the county information
            parish - string with the parish information
            farm_nums - string with semi-colon separated list of farm numbers
            ref - string with unique record string
            
        Outputs:
            Set with generated farm number (only one number is expected)
    
    '''
    generated_farm_numbers = generate_farm_numbers(county, parish, farm_nums)
    
    farm_generated_number = set()
    
    for generated_number in generated_farm_numbers:
        if ref[-1] == generated_number[-1]:
            farm_generated_number.add(generated_number)       
        
    return farm_generated_number


def generate_farm_numbers(county, parish, farm_nums):
    ''' Generates a unique farm numbers from the county code, parish code and farm number
    
        Keyword Arguments:
            county - string with the county information
            parish - string with the parish information
            farm_nums - string with semi-colon separated list of farm numbers
            
        Outputs:
            Set with generated farm numbers
    
    '''
    county_code = county.split(" ")[0]
    parish_num = parish.split(" ")[0]
    
    farm_numbers = set()
    
    for farm_num in farm_nums.split(";"):
        farm_numbers.add(county_code + "/" + parish_num + "/" + farm_num)
    
    return farm_numbers
    

# Group 4: Farm
# Input column: H (farm_name)
# Expecting 2 rows of data
# Check 1: values should be similar, ignoring asterisk and blanks. Return combined value.
# Return combined value [Output column: G (Farm Name)]  
# Warning: if not similar [Output column: H (Farm Name Warnings)]
# Warnings if unexpected number of rows matched   

def get_combined_farm_names_by_ref(farm_names):
    ''' Creates a combined value for the farm name from the list of names given for a particular farm
    
        Keyword Arguments: 
            farm_names - dictionary with list of farm names for each farm using the farm reference as the key
            
        Outputs:
            Tuple with dictionary of combined name value for each farm, and a dictionary of with a set of warnings for each farm
    '''
    
    combined_names, warnings = dn.component_compare(farm_names)
    
    for ref in farm_names.keys(): 
        count = len(farm_names[ref])
        if count != 2:
            warnings[ref].add("Expected 2 rows of data, Got " + str(count) + ".")
    
    return (combined_names, warnings)


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

def get_combined_owner_details_by_ref(owner_details):
    ''' Combines owner values and flags warnings if unexpected values found
    
        Key Arguments:  
            owner_details - dictionary with each reference key containing a dictionary with the following: key: 'Title' - list of string values, 'Individual Name' - list of string values, 'Group Names' - list of lists with string values and 'Addresses' - list of lists with string values
            
        Returns:
            Tuple with a dictionary with the combined values for each field by reference and a dictionary with a set of warnings for each reference
    '''
    return get_combined_details_by_ref(owner_details, 1)


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

def get_combined_farmer_details_by_ref(farmer_details, addressee_details):
    ''' Combines owner values and flags warnings if unexpected values found
    
        Key Arguments:  
            farmer_details - dictionary with each reference key containing a dictionary with the following: key: 'Title' - list of string values, 'Individual Name' - list of string values, 'Group Names' - list of lists with string values and 'Addresses' - list of lists with string values
            addressee_details - dictionary with each reference key containing a dictionary with the following: key: 'Title' - list of string values, 'Individual Name' - list of string values, 'Group Names' - list of lists with string values and 'Addresses' - list of lists with string values
                        
        Returns:
            Tuple with a dictionary with the combined values for each field by reference and a dictionary with a set of warnings for each reference
    ''' 

    warnings = {}
    combined_details = {}
    components = ["Title", "Individual Name", "Group Names", "Addresses"]
    
    # Create combined values by getting similar values for each field
    # call get_combined_details_by_ref with combined values  
    
    shared = set()
    farmer_only = set()
    addressee_only = set()
    
    if farmer_details.keys() != addressee_details.keys():
        shared = set(farmer_details.keys()).intersection(set(addressee_details.keys()))
        farmer_only = set(farmer_details.keys()) - set(addressee_details.keys())
        addressee_only = set(addressee_details.keys()) - set(farmer_details.keys())
    else:
        shared = set(farmer_details.keys())
    
    for ref in list(shared):
        combined_details[ref] = {}
        warnings[ref] = set()
        farmer_title = farmer_details[ref]["Title"]
        farmer_name = farmer_details[ref]["Individual Name"]
        farmer_groups = farmer_details[ref]["Group Names"]
        farmer_addy = farmer_details[ref]["Addresses"]
        
        addressee_title = addressee_details[ref]["Title"]
        addressee_name = addressee_details[ref]["Individual Name"]
        addressee_groups = addressee_details[ref]["Group Names"]
        addressee_addy = addressee_details[ref]["Addresses"]   
        
        combined_details[ref].update({"Title": farmer_title + addressee_title})
        combined_details[ref].update({"Individual Name": farmer_name + addressee_name})  
        combined_details[ref].update({"Group Names": farmer_groups + addressee_groups})
        combined_details[ref].update({"Addresses": farmer_addy + addressee_addy})    
           
    
    for ref in list(farmer_only):
        combined_details[ref] = {}
        warnings[ref] = set()
        combined_details[ref].update({"Title": farmer_title})
        combined_details[ref].update({"Individual Name": farmer_name})  
        combined_details[ref].update({"Group Names": farmer_groups})
        combined_details[ref].update({"Addresses": farmer_addy})  
        warnings[ref].add("No addressee values given")
    
    for ref in list(addressee_only):
        combined_details[ref] = {}
        warnings[ref] = set()
        combined_details[ref].update({"Title": addressee_title})
        combined_details[ref].update({"Individual Name": addressee_name})  
        combined_details[ref].update({"Group Names": addressee_groups})
        combined_details[ref].update({"Addresses": addressee_addy}) 
        warnings[ref].add("No farmer values given") 
    
    #print("Farmer Details:")
    #print(farmer_details)
    #print()
    #print("Addressee Details:")
    #print(addressee_details)
    #print()
    #print("Combined Details:")
    #print(combined_details)
    
    threshold = 80
    for ref in combined_details.keys():
        for component in components:
            min = dn.get_similarity_range(combined_details[ref][component], get_max=False)
            if min < threshold:
                warnings[ref].add("Similarity (" + str(min) + ") below threshold (" + str(threshold) + ") for " + component) 
        
    
    combined_values, combined_warnings = get_combined_details_by_ref(combined_details)
    
    warnings = dic_merge(warnings, combined_warnings)
    #print(warnings)
    
    return (combined_values, warnings)
        
    
def get_combined_details_by_ref(details, expected_count = -1):
    ''' Combines title, individual name, group name and addressee values as either "title individual name, address" or "group name, address", where there may be multiple group names and addresses, and flags warnings if unexpected values found.
    
        Key Arguments:  
            details - dictionary with each reference key containing a dictionary with the following: 
                    reference:  'Title' - list of string values, 
                                'Individual Name' - list of string values, 
                                'Group Names' - list of lists with string values, and 
                                'Addresses' - list of lists with string values
            expected_count - optional integer. If positive integer in given then a check is carried out on the number of rows with with data
                        
        Outputs:
            Tuple with a dictionary with the combined values for each field by reference, and a dictionary with a set of warnings for each reference
    '''
          
    warnings = {}
    combined_details = {}
    components = ["Title", "Individual Name", "Group Names", "Addresses"]
    
    titles = {}
    names = {}
    groups = {}
    addresses = {}
    
    for ref, detail in details.items(): 
        warnings[ref] = set()
        #print(details)
        
        '''
        # lists of strings as single value expected
        titles[ref] = "/".join(details["Title"])
        names[ref] = "/".join(details["Individual Name"])
        # lists of lists because multiple values allowed
        for gname in details["Group Names"]:
            if ref in groups.keys():
                groups[ref] += "/".join(gname)
            else:
                groups[ref] = "/".join(gname)
        for addy in details["Addresses"]:
            if ref in addresses.keys():
                addresses[ref] += "/".join(addy)
            else:
                addresses[ref] = "/".join(addy)
        '''

        count = set()
        #for each type of field e.g. Title, Individual Name etc converts values to single string for each
        for component in components:
            component_length = len(detail[component]) 
            count.add(component_length)
            values_to_merge_dict = {}
            
            if component_length > 1: # Check if there is more that one variation and if so merge
                
                if component == "Group Names" or component == "Addresses":
                    values_to_merge_dict = array_zip(detail[component], component)
                else:
                    values_to_merge_dict[component] = detail[component]
                    #for i, values in enumerate(detail[component]):
                    #        values_to_merge_dict[component+str(i)] = [values]
                     
                merged_values, merge_warnings = dn.component_compare(values_to_merge_dict)
                
                for warning in merge_warnings.values():
                    if len(warning) > 0:
                        warnings[ref].update(warning)
                
                if component == "Title":
                    titles[ref] = list(merged_values.values())
                elif component == "Individual Name":
                    names[ref] = list(merged_values.values())
                elif component == "Group Names":
                    groups[ref] = list(merged_values.values())
                elif component == "Addresses":
                    addresses[ref] = list(merged_values.values())
                else:
                    print("Error in get_combined_details_by_ref: unknown component type: " + component)  
            else: # If there are not multiple variations then get first value
                if component == "Title":
                    titles[ref] = detail[component][0]
                elif component == "Individual Name":
                    names[ref] = detail[component][0]
                elif component == "Group Names":
                    groups[ref] = detail[component][0]
                elif component == "Addresses":
                    addresses[ref] = detail[component][0]  
     
            
        if len(count) != 1: #Check how many distinct counts are in the set - should only be one as should be the same number of values for each component
            warnings[ref].add("Mismatch in number of expected answers.")    
        
        count_list = list(count)  
        # if a positive value is give for expected_count then check the if there is more than one value in the list or if the first (should be only) value does not match the expected_count 
        if expected_count > 0 and (count_list[0] != expected_count or len(count_list) != 1):
            if len(count_list) != 1:
                warnings[ref].add("Expected " + str(expected_count) + " row of data, Got " + str(count_list.sort()[0]) + "-" + str(count_list.sort()[-1] + "."))             
            else:
                warnings[ref].add("Expected " + str(expected_count) + " row of data, Got " + str(count_list[0]) + ".")
                
    for ref in details.keys():  
        name = ""  
        
        name_value = names[ref]
        title_value = titles[ref]
        group_value = groups[ref]
        addy_value = addresses[ref] 
        
        if isinstance(name_value, list):
            temp = set(name_value)
            if len(temp) == 1 and (list(temp)[0] == ""):
                name_value = ""
            elif len(temp) == 1:
                name_value = list(temp)[0]
            else:
                warnings[ref].add("Error: multiple names found when one expected")
                name_value = "/".join(name_value) 

        if isinstance(title_value, list):
            temp = set(title_value)
            if len(temp) == 1 and (list(temp)[0] == ""):
                title_value = ""
            elif len(temp) == 1:
                title_value = list(temp)[0]                
            else:
                warnings[ref].add("Error: multiple names found when one expected")
                title_value = "/".join(title_value) 

        if isinstance(group_value, list):
            temp = set(group_value)
            if len(temp) == 1 and (list(temp)[0] == "" or list(temp)[0] == "*"):
                group_value = group_value[0]
        
        if name_value != "*" and name_value != "":
            #name
            if title_value != "*":
                name = title_value + " " + name_value

            name = name.strip() 
            
            if isinstance(group_value, list):  
                warnings[ref].add("Error: values found in both name (" + name_value + ") and groups (" + ";".join(group_value) + ")")    

            # Address            
            address = ""
            if isinstance(addy_value, list) and len(addy_value) > 1:
                warnings[ref].add("Error: multiple addresses found when one expected") 
                address = "/".join(addy_value)  
            elif isinstance(addy_value, list):
                address = addy_value[0]
            else:
                address = addy_value
                
            if address == "*":
                address = "[..?]"
                
            combined_details[ref] = name + ", " + address  
            
        else:  
            group_names = []                 
            if isinstance(group_value, list) and isinstance(addy_value, list): 
                if len(group_value) != len(addy_value):
                    warnings[ref].add("Error: Length of group names (" + str(len(group_value))+ ") and addresses (" + str(len(addy_value)) + ") different") 
                
                for i, group in enumerate(group_value):
                    group = group.strip()
                    if group == "*":
                        group = "[..?]"
                        
                    if i < len(addy_value) and addy_value[i].strip() != "":
                        addy = addy_value[i]
                        if addy.strip() == "*":
                            addy = "[..?]"
                        group_names.append(group + ", " + addy)
                    else:
                        group_names.append(group)  
                        warnings[ref].add("Warning: No address with " + group)   
                        
                if len(addy_value) > len(group_value):
                    for i in range(len(group_value) - 1, len(addy_value)):
                        addy = addy_value[i]
                        if addy.strip() == "*":
                            addy = "[..?]"
                        group_names.append("[..?], " + addy)
                        warnings[ref].add("Warning: No group name with " + addy)                
                 
            else:
                print("get_combined_details_by_ref: Expecting lists for group and address values")
                
            combined_details[ref] = "; ".join(group_names)
               
    #print(combined_details) 
    #print(warnings)           
        
    return(combined_details, warnings)      


def array_zip(details_array, key = ""):
    ''' Takes a dictionary with an array of arrays and zips the arrays together, extending the shorter array if necessary
    
        Key Arguments:
            details_array - dictionary containing and array of arrays in the values
            key - optional string to be added to the key in the returned dictionary
            
        Returns:
            Dictionary with the same keys as the input but with each component in the original lists zipped together
    '''
    
    values_to_merge_dict = {}
    longest = 0  
    
    for part in details_array:
        if len(part) > longest:
            longest = len(part)
    
    for i in range(0, len(details_array)):
        while len(details_array[i]) < longest:
            details_array[i].append("") 
            
    values_to_merge = list(zip(*details_array))
    
    for i, values in enumerate(values_to_merge):       
        values_to_merge_dict[key + str(i)] = list(values)
        
    return values_to_merge_dict


def dic_merge(dic1, dic2):
    ''' Deep merge of two dictionaries
    
        Key Arguments:
            dic1 - nested dictionary 
            dic2 - nested dictionary
            
        Outputs:
            Merged dictionary
    '''
    
    merged_dic = {}
    merged_keys = set(dic1.keys()).union(set(dic2.keys()))
    
    for key in merged_keys:
        if key in dic1 and key in dic2:
            if isinstance(dic1[key], dict) and isinstance(dic2[key], dict):
                merged_dic[key] = dic_merge(dic1[key], dic2[key])
            elif isinstance(dic1[key], set) and isinstance(dic2[key], set):  
                merged_dic[key] = dic1[key].union(dic2[key])
            elif isinstance(dic1[key], list) and isinstance(dic2[key], list): 
                merged_dic[key] = dic1[key] + dic2[key]
            else:
                merged_dic[key] = dic1[key]
                merged_dic[key].update(dic2[key])
                
        elif key in dic1:
            merged_dic[key] = dic1[key]
        else:
            merged_dic[key] = dic2[key]
    
    return merged_dic


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

def date_processing(field_date, primary_dates, row_num):
    ''' Checks if dates are valid and that field date occurred before primary date(s)
    
        keyword Arguments: 
            field_date - string with the date of the field information
            primary_dates - semi-colon separated string with the date or dates of the primary records
            row_num - string with the number of the row in the source spreadsheet
            
        Outputs:
            Tuple of tuples. The first tuple contains a string with the field date value and a set of warnings related to the field dates, the second tuple contains the same but for the primary dates.
    '''
    
    if not(field_date == "" or field_date == "*"):
        checked_field_date, field_date_warnings = date_check(field_date, row_num)
    else:
        checked_field_date = ""
        field_date_warnings = set()
    
    primary_date_warnings = set()
    primary_date_list = []
    
    if type(checked_field_date) is datetime.datetime:
        checked_field_date_str = checked_field_date.strftime('%d %B %Y')
        #print("Checked field date is datetime. String version is " + checked_field_date_str)
    else:
        checked_field_date_str = checked_field_date
        #print("Checked field date is not datetime. String version is " + checked_field_date_str)
    
    if len(primary_dates.split(";")) > 1:
        primary_date_warnings.add("Row " + row_num + ": Multiple dates listed.")
    
    for primary_date in primary_dates.split(";"):
        if not(primary_date == "" or primary_date == "*"):
            checked_primary_date, pdate_warning = date_check(primary_date, row_num)
            
            if type(checked_primary_date) is datetime.datetime:
                checked_primary_date_str = checked_primary_date.strftime('%d %B %Y')
            else:
                checked_primary_date_str = checked_primary_date
            
            primary_date_warnings.update(pdate_warning)
            primary_date_list += [checked_primary_date_str]            
            
            if type(checked_primary_date) is datetime.datetime and type(checked_field_date) is datetime.datetime and checked_primary_date < checked_field_date:
                date_warning = "Row " + row_num + ": Error - Primary Date (" + checked_primary_date_str + ") earlier than Field date (" + checked_field_date_str + ")"
                field_date_warnings.add(date_warning)
                primary_date_warnings.add(date_warning)
                   
    return ((checked_field_date_str, field_date_warnings), (", ".join(primary_date_list), primary_date_warnings))        
    

def date_check(potential_date, row_num):    
    ''' Checks if the date, given as a string, is a valid date
    
        Keyword Arguments:
            potential_date - string containing the date value for checking
            row_num - string with the number of the row in the source spreadsheet
            
        Returns:
            Tuple with either the date as a date object or the original string if it isn't a valid date and a set with any warnings
    '''
    
    warnings = set()
    potential_date = potential_date.strip()

    #print(row_num + ": " + potential_date)
    try:
        if "-" in potential_date:
            day = int(potential_date.split("-")[0])
            month = potential_date.split("-")[1]
            year = potential_date.split("-")[2]
        elif " " in potential_date:
            day = int(potential_date.split(" ")[0])
            month = potential_date.split(" ")[1]
            year = potential_date.split(" ")[2]
        elif "/" in potential_date:
            day = int(potential_date.split("/")[0])
            month = potential_date.split("/")[1]
            year = potential_date.split("/")[2]   
            
    except ValueError as ve:
        warnings.add("Row " + row_num + ": Error - Date (" + potential_date + ") is not recognized as a valid date in the expected format (" + str(ve) + "). Further date checks cannot be carried out.")
        return (potential_date, warnings)   
        
          
    if len(year) == 2:
        year = int(year)
        year += 1900
    elif len(year) != 4:
        warnings.add("Row " + row_num + ": Error - Date (" + potential_date + ") is not recognized as within the expected range.")
        
    year = int(year)
    
    if month.isdigit():
        month_number = int(month)
    else:
        try:
            month_number = datetime.datetime.strptime(month, '%B').month
        except ValueError as ve:
            try:
                month_number = datetime.datetime.strptime(month, '%b').month
            except ValueError as ve:
                month_number = 0    
            
            warnings.add("Row " + row_num + ": Warning - Month (" + month + ") is not in the expected format.") 
                    
    try:
        date = datetime.datetime(year=year,month=month_number,day=int(day))  
         
    except ValueError as ve:
        warnings.add("Row " + row_num + ": Error - Date (" + potential_date + ") is not recognized as a valid date in the expected format (" + str(ve) + "). Further date checks cannot be carried out.")
        date = potential_date
        
    return (date, warnings)
            


processing_folder = "processing"
load_spreadsheet_data(processing_folder)