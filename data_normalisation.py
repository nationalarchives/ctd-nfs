# Compare and normalise data from multiple columns
#   
#   Select columns to compare
#   Put values into Set to see how many unique values there are
#   Tokenize each words
#   Check number of tokens
#   If there are more then one then check distribution
#   
#

from rapidfuzz import fuzz
import difflib, re


def component_compare (values_to_check, debug = False):
    ''' Function to compare the components
    
        Keyword arguments:
        values_to_check - a dictionary of values made up of a key and a list of components
        debug - boolean, False by default, if True print out debug
        
        Returns
            Dictionary with key references taken from the input and a string value with the combined values of the related components
        
    '''
    combined_values = {}
    warnings = {}
    
    for key, component_list in values_to_check.items():
        component_set = set([component for component in component_list if (component.strip() != "" and component.strip() != "*")])
        
        #print(component_set)
        #distribution = split_distribution(component_list)
        distribution = split_part_distribution(component_list)
        warnings[key] = set()

        if len(component_set) < 2:  # One version
            basic_join = "".join([component for component in component_set])
            if debug:
                print("Basic join - " + key + ": " + basic_join)
            combined_values[key] = basic_join
        elif len(component_set) == 2:   # Two variations
            two_phrase_join, two_phrase_join_warnings = combine_two_phrases(key, component_set, distribution, debug)
            warnings[key].update(two_phrase_join_warnings)
            if debug:
                print("Two part join - " - key + ": " + two_phrase_join)
            combined_values[key] = two_phrase_join
        else:   # More than two variations
            
            #print(component_set)
            warnings[key].add("Complex variations.")
            distinct = []
            
            for component1 in component_set:
                max_ratio = 0
                for component2 in component_set:
                    if component1 != component2:
                        ratio = fuzz.ratio(component1, component2)
                        if ratio > max_ratio:
                            max_ratio = ratio
                        #print(component1 + "-" + component2 + ": " + str(ratio))
                
                if max_ratio < 50:
                    distinct.append(component1) 
                    
            similar = component_set - set(distinct)
            
            similar_list =[component for component in component_list if component in similar]
            #print("Similar list")
            #print(similar_list)
            subset_distribution = split_part_distribution(similar_list)
            
            if len(similar) == 2:
                #print(key + ": Option E")
                #print(similar)
                #print(distinct) 
                combined_phrases, sub_set_warnings = combine_two_phrases(key, similar, subset_distribution, debug)
                warnings[key].update(sub_set_warnings)
                if debug: 
                    print("Complex join - " + key + ": " + combined_phrases + " (" + "? ".join(distinct) + "?)")  
                    
                combined_values[key] = combined_phrases + " (" + "? ".join(distinct) + "?)"           
            elif len(similar) == 3:
                if debug:
                    print(key + ": Option F")  
                combined = {}
                for component1 in similar:
                    for component2 in similar:
                        if component1 != component2:
                            ratio = fuzz.ratio(component1, component2)
                            print(component1 + "-" + component2 + ": " + str(ratio))
                            if ratio > 85:
                                combined_string, sub_set_warnings = combine_two_phrases(key, {component1, component2}, subset_distribution, debug)
                                warnings[key].update(sub_set_warnings)
                                combined[combined_string] = re.sub("[()]", "", combined_string)
                                
                #print(combined)
                if len(combined) > 1:    
                    print(split_part_distribution(set(combined.values())))
                    combined_values[key] = split_part_distribution(set(combined.values()))    
           
            elif len(similar) == 4:
                if debug:
                    print(key + ": Option G")  
                combined_values[key] = "/".join(component_list)             
            else:
                if debug:
                    print(key + ": Option H")
                combined_values[key] = "/".join(component_list) 
                
    return (combined_values, warnings)
                
            
    
                
                    


def split_distribution (component_list):
    ''' Calculates the distribution of a pair of variations
        
        Keyword arguments:
        component_list - list of components
        
        return a dictionary with the counts for each version
    '''
    component_distribution = {}
    
    
    for component in component_list:
        if component in component_distribution.keys():
            component_distribution[component] = component_distribution[component] + 1
        else:
            component_distribution[component] = 1
            
    return component_distribution

def split_part_distribution (component_list):
    ''' Calculates the distribution of variation parts
        
        Keyword arguments:
        component_list - list of components
        
        return a dictionary with the counts for each part in the components
    '''
    component_distribution = {}
    
    
    for component in component_list:
        for part in component.split(" "):
            if part in component_distribution.keys():
                component_distribution[part] = component_distribution[part] + 1
            else:
                component_distribution[part] = 1
                
    #print(component_distribution)
            
    return component_distribution


def get_tokens (component_set):
    ''' split the components into words
    
        Keyword arguments:
        component_set - set of components 
        
        return a tuple containing a list of components and a list of the lengths of those components
    '''
    tokens = []
    count_set = set()
    for component in component_set:
        tokenized_component = component.split(" ")
        tokens.append(tokenized_component)
        count_set.add(len(tokenized_component))
              
    return (tokens, list(count_set))   

def combine_two_phrases(key, component_set, distribution, debug):
    #print(key + ": " + ", ".join([component for component in component_set]))
    #print(key + ": ")

    split_components, count_of_component_lengths = get_tokens(component_set)
    warnings = set()
    #print(split_components)
    #print(count_of_component_lengths)
    
    if len(count_of_component_lengths) < 2: # all variants are the same number of parts
        #print("Combine two phrases")
        
        generated_component = ""
        for part in range (0, count_of_component_lengths[0]):  # looping over each part                                    
            
            parts = {split_components[variant][part]: len(split_components[variant][part]) for variant in range (0, len(split_components))}
            #print(parts)
            
            if 1 in parts.values(): #if name parts contain a 1 letter component or components (i.e. initials)
                initials = list(set([part[0] for part in parts.keys()])) # create set of first letters
                
                if len(initials) < 2: #if initials and first letters match 
                    non_initials = list(set([part for part in parts.keys() if len(part) > 1])) #compare components that aren't 1 letter
                    #print(non_initials)
                    
                    if len(non_initials) == 1:
                        generated_component += " " + non_initials[0]
                    elif len(non_initials) < 1:
                        generated_component += initials[0]
                        
                    warnings.add("Combining initial and names.")
                else:
                    #print("Option A")
                    generated_component += " " + combine_two_words(list(parts.keys())[0], list(parts.keys())[1], distribution, debug)
                    #print(parts)
                
            elif len(parts.keys()) < 2: # component tokens are the same
                generated_component += " " + list(parts.keys())[0]
            elif len(parts.keys()) == 2: # if there are two variations
                generated_component += " " + combine_two_words(list(parts.keys())[0], list(parts.keys())[1], distribution, debug)
                warnings.add("Combining variations.")
            else: # if there are more than two versions
                print(key + ": Option C")
                warnings.add("Combining variations.")
                    
        #print(key + ": " + generated_component.strip())
        return (generated_component.strip(), warnings)
    
    else:
        #print("Option D")
        #print(key + ": " + align_two_phrases(split_components[0], split_components[1], distribution)) 
        #print("Align two phrases")
        warnings.add("Combining multi-length variations.")
        return (align_two_phrases(split_components[0], split_components[1], distribution), warnings)  


def combine_two_words (component1, component2, word_ratio, debug = False):
    ''' Combine two words
    
        Keyword arguments:
        component1 - single word string
        component2 - single word string
        word_ratio - dictionary of variation ratio
        
        returns string with combined values
    '''
    
    ratio = fuzz.ratio(component1, component2)
    if ratio > 85: # if the variations are similar
        #generated_component += " " + list(parts.keys())[0] + "/" + list(parts.keys())[1]
        diff = difflib.Differ().compare(component1, component2)
        
        generated_string = [s.strip() if s[0] == ' ' else '(' + s[-1] + ')' for s in diff]
        return ''.join(generated_string)
    else:
        #print("Option B: " + str(ratio))
        
        component1_count = 0
        component2_count = 0
        
        for key in word_ratio:
            if component1 == key:
                component1_count = word_ratio[key]
                
            if component2 == key:
                component2_count = word_ratio[key]
        
        #print(component1 + ": " + str(component1_count))
        #print(component2 + ": " + str(component2_count))
            
        
        if component1_count > component2_count:
            generated_string =  component1 + " (" + component2 + "?)"
        elif component2_count > component1_count:
            generated_string =  component2 + " (" + component1 + "?)"
        else:
            comp_list = [component1, component2]
            generated_string = "/".join(sorted(comp_list, key=str.lower))
            
        if debug:
            print(generated_string)
        
        return ''.join(generated_string)


def align_two_phrases(string1, string2, word_ratio, debug = False):
    ''' Check if two strings align and return a combined version

        keyword arguments:
        string 1 - the first phrase
        string 2 - the second phrase
        word_ratio - dictionary of variation ratio
        
        returns string with combined values
    '''
    #diff = difflib.Differ().compare(string1, string2)
    #print("\n".join(diff))
    
    components1, components1_sizes = get_tokens(string1)
    components2, components2_sizes = get_tokens(string2)
    
    combined = ""
    
    #print(components1)
    #print(components2)
    
    if len(components1) > len(components2):
        return get_match_matrix(components1, components2, word_ratio, debug)
    else:
        return get_match_matrix(components2, components1, word_ratio, debug)
    


def get_match_matrix(longest, shortest, word_ratio, debug = False):
    ''' get the comparison matrix
    
        keyword arguments:
        longest - the longest list 
        shortest - the shortest list
        word_ratio - dictionary of variation ratio
        
        return 
    '''
    match_matrix = {}
    
    for i in range(0, len(longest)):
        match_matrix[i] = {j: fuzz.ratio(longest[i][0], shortest[j][0]) for j in range(0, len(shortest))}
        
    combined = []
    
    checking = True
    x = 0
    y = 0
    
    while x < len(longest) and checking: 
        #best_match_ratio = max(match_matrix[i].values())
        #number_of_best_matches = list(match_matrix[i].values()).count(best_match_ratio)   
        #print("x:" + str(x))
        #print("y:" + str(y))
        #print("longest:" + str(len(longest)))
        
        sorted_options = dict(sorted(match_matrix[x].items(), key=lambda item: item[1], reverse=True))        
        
        #print(sorted_options)
        best_match_ratio = max(list(sorted_options.values()))
        
        if best_match_ratio < 1: # there is no match
            combined.append("(" + longest[x][0] + ")")
            
            if x <= len(longest):
                x += 1                       
        else:
            best_match_longest = longest[x]
            
            not_assigned = True
            m = 0            
            while not_assigned and m < len(shortest):
                if list(sorted_options.keys())[m] > y:   
                    y = list(sorted_options.keys())[0]
                    not_assigned = False
                else:
                    m += 1
                    
            best_match_shortest = shortest[y]
            
            #print(best_match_longest[0])
            #print(best_match_shortest[0])
            
            combined.append(combine_two_words(best_match_longest[0], best_match_shortest[0], word_ratio))
            
            if x <= len(longest):
                x += 1
            
            #print("x:" + str(x) + " / " + str(len(longest)))         
            #print(combined) 
            
            #print("x:" + str(x) + " / " + str(len(longest)))      
            #print(combined) 
    
    if debug:
        print(combined)  
    return ' '.join(combined) 
        
    #print(match_matrix)
    
    
def split_address(address):
    pass
        

'''
names = {"1":["H Arkell", "H Arkell", "H Arkell", "H Arkell"], 
         "2":["", "W H Buckle", "W H Buckle", "W H Buckle"], 
         "3":["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
         "6":["A E Cook", "A E Cook", "A E Cook", "A E Cook"],
         "7":["A G Griffiths", "W L Edmunds", "W L Edmunds", "W L Edmunds"],
         "9":["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"],
         "10":["", "F W Hinton", "", "F W Hinton"],
         "14":["G P Rymer", "G P Rymer", "G P Rymer", "G P Rymer"],
         "15":["A Spragg", "A Spragg", "A Spragg", "A Spragg"],
         "16":["H Bowl", "Harry Bowl", "H Bowl", "Harry Bowl"],
         "18":["A Tombs", "A Tombs", "A Tombs", "A Tombs"],
         "19":["C Tombs", "C Toombs", "C Toombs", "C Toombs"],
         "20":["G O Tombs", "G O Tombs", "G O Tombs", "G O Tombs"],
         "22":["G Wilkins", "G Wilkins", "Geo Wilkin", "G Wilkins"],
         "31":["", "F Bendall", "F Bendall", "F Bendall"],
         "33":["F Thomas", "Frank Thomas", "F Thomas", "Frank Thomas"]
         }
'''
names = {#"1": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
         #"2": ["R Burroughs", "R Burroughs", "R Burroughs", "R Burroughs"],
         #"3": ["R Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
         "4": ["R Burroughs", "J Burroghs", "J Burroughs", "R Burroughs"], 
         #"5": ["R J Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"],
         #"6": ["J R Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"], 
         #"7": ["J R Burrows", "J Burroughs", "J Burroughs", "J Burroughs"], 
         #"8": ["R J Burroughs", "R L Burroughs", "R Burroughs", "R Burroughs"],
         #"9": ["R J Burrows", "R L Burroughs", "J Burroughs", "J Burroughs"],
         #"10": ["R J Burrows", "R L Burroughs", "R Burroughs", "R Burroughs"],
         #"11": ["R Burrows", "R Burroughs", "R Burroughs", "F Rymer"],
         #"12": ["R Burrows", "R Burroughs", "R Burroughs", "R Rymer"],
         #"13": ["R Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
         #"14": ["R Burrows", "R F Burroughs", "R Burroughs", "F Rymer"],
         #"15": ["R J Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
         "16": ["R J Burrows", "R Burroughs", "R Burroughs", "R J Burroghs"],
         #"17": ["R J Burrows", "A E Cook", "G P Rymer", "Geo Wilkin"],
         #"18": ["R J Burrows", "R Burroughs", "G P Rymer", "Geo Wilkin"],
         #"19": ["R J Burrows", "R Burroughs", "R Burroghs", "R J Burroghs"],
         #"17": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"]                   
        }


address = {"1":["Butlers Court Farm, Boddington, Gloucestershire", "Butlers Court, Boddington, Near Cheltenham", "Butlers Court, Boddington", "Butlers Court Farm, Boddington, Gloucestershire"], 
         "2":["Whitehall, Hayden Hill, Cheltenham, Gloucestershire", "Whitehall Farm, Hayden, Cheltenham", "Whitehall Farm, Hayden, Cheltenham", "Whitehall, Hayden Hill, Cheltenham, Gloucestershire"], 
         "3":["Boddington House Farm, Boddington, Gloucestershire", "Boddington House Farm, Boddington, Cheltenham", "Boddington House Farm, Near Cheltenham", "Boddington House, Boddington, Gloucestershire"],
         "6":["Slate Mill, Boddington, Near Cheltenham, Gloucestershire","Slade Mill, Boddington, Cheltenham", "Slate Mill, Boddington", "Slate Mill, Boddington, Near Cheltenham, Gloucestershire"],
         "7":["Barrow Court, Boddington, Cheltenham, Gloucestershire", "14, Foregate Street, Worcester", "Barrow Court, Boddington", "Barrow Court, Boddington, Cheltenham, Gloucestershire"],
         "9":["Manor Farm, Boddington, Near Cheltenham, Gloucestershire", "Guiting House, Temple Guiting, Gloucestershire", "Manor Farm, Boddington", "Manor Farm, Boddington, Near Cheltenham, Gloucestershire"],
         "10":["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "192 High Street, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
         "14":["14 Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, Charlton Kings, Cheltenham", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
         "15":["Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire", "Mill House Farm, Boddington, Near Cheltenham", "Withybridge Farm, Boddington", "Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire"],
         "16":["Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire", "Barrow Hill Farm, Boddington, Cheltenham", "Barrow Hill Farm, Boddington", "Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire"],
         "18":["Brookes Laymes Farm, Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Brookes Laymes Farm, Boddington", "Brookes Laymes Farm, Boddington, Gloucestershire"],
         "19":["Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Boddington", "Boddington, Gloucestershire"],
         "20":["Hayden Farm, Boddington, Near Cheltenham, Gloucestershire", "Hayden Farm, Hayden, Cheltenham", "Hayden Farm, Boddington", "Hayden Farm, Boddington, Near Cheltenham, Gloucestershire"],
         "22":["Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire", "Wilkins Farm, Boddington, Cheltenham", "Wilkins Farm, Barrow, Boddington", "Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire"],
         "31":["1 Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire", "1 Hayden Hill Villas, Hayden Hill, Boddington", "Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire"],
         "33":["Pilgrove, Hayden Hill, Near Cheltenham, Gloucestershire", "Pilgrove, Hayden Hill, Boddington, Gloucestershire", "Pilgrove, Hayden Hill, Cheltenham", "Pilgrove, Hayden Hilll, Near Cheltenham, Gloucestershire"]
         }

farm_name = {"1":["*", "Holt Farm", "", ""], 
         "2":["*", "Park Valley Farm", "", ""], 
         "3":["Home Farm", "Serge Hill", "", ""],
         "4":["Buckmans Farm etc", "Cuckmans Farm", "", ""],
         "5":["Old Parkbury Farm", "Old Parkbury", "", ""],
         "6":["*", "Netherwylde Farm", "", ""],
         "8":["*", "Smug Oak Farm", "", ""],
         "9":["*", "Garston Manor", "", ""],
         "10":["*", "Silver Birches", "", ""],
         "11":["*", "Spooners", "", ""],
         "12A":["", "Land at Ninnings Farm", "", ""],
         "12B":["Millhouse Farm", "Millhouse Farm", "", ""],
         "13":["*", "Harperbury", "", ""],
         "17":["*", "Land at Park Street", "", ""],
         "18":["*", "Home Farm", "", ""],
         "19":["Little Munden Farm", "Little Munden Farm", "", ""],
         "20":["Noke Farm", "Noke Farm", "", ""]
         }


#component_compare(names)