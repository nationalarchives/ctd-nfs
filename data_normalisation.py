# Compare and normalise data from multiple columns
#   
#   Select columns to compare
#   Put values into Set to see how many unique values there are
#   Tokenize each words
#   Check number of tokens
#   If there are more then one then check distribution
#   
#

# Functions:
#   component_compare (values_to_check, debug=False)
#   punctuated_title(to_convert)
#   to_upper(match)
#   to_lower(match)
#   ratio_check(length, ratio)
#   split_distribution (component_list)
#   split_part_distribution (component_list)
#   token_distribution (component_list, tokens, debug=False)
#   get_tokens (component_set)
#   combine_connected_letters(list_to_test, string_to_compare)
#   chunk_punctuated_string(string_to_process, all=True)
#   combine_two_phrases(component_set, component_list, debug=False)
#   combine_two_words (component1, component2, word_ratio, debug=False)
#   get_context(letter_group, phrase_string)
#   align_two_phrases(string1, string2, component_list, debug=False)
#   clean_string(string_to_clean)
#   clean_brackets(string_to_clean)
#   initials_replace(phrase_to_be_processed, phrase_for_comparison, debug=False)
#   get_match_ratios(phrase1, phrase2, debug = False)
#   get_match_matrix(first_phrase, second_phrase, component_list, debug=False)

#####################
#   To Do:
#   
#   
#   Need to do more testing with phrases espec. of different lengths - maybe do need to do the check merging both ways
#   See if there is a better way to check mismatches based on match level of chunks since addresses with extra information are incorrectly identified as a mismatch.
#   In component_compare - code for the case 'len(component_set_caseless) > 2' hasn't been implemented
#   In combine_two_words - code for the case 'substr_count is > 1' hasn't been implemented

from rapidfuzz import fuzz
import difflib, re


def component_compare (values_to_check, debug=False):
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
        
        warnings[key] = set()
        component_set = set([component for component in component_list if (component.strip() != "" and component.strip() != "*")])   
        #component_list_caseless = [component.lower() for component in component_list if (component.strip() != "" and component.strip() != "*")]   
        alt_component_set = set([("".join(component.split())).lower() for component in component_list if (component.strip() != "" and component.strip() != "*")] )


        # does the default set have the same number of values as the set with all the spaces and cases removed
        if len(component_set) != len(alt_component_set):
            component_set_caseless = set([component.lower() for component in component_list if (component.strip() != "" and component.strip() != "*")])  
                     
            # does the default set and the caseless set not have the same length while the caseless and the space+caseless have the same length
            if len(component_set) != len(component_set_caseless) and len(alt_component_set) == len(component_set_caseless):
                #print("Case Issue")
                
                #Assumption: Case mismatch - convert to title case.
                component_set = {punctuated_title(item) for item in component_set}
                
                #print(component_set)
            
                '''
                for i in range(0, len(diff_list)):
                    
                    if diff_list[i][0] != ' ' and i > 0 and diff_list[i-1].strip() == '':
                        if i+1 < len(diff_list) and diff_list[i][-1].lower() == diff_list[i+1][-1].lower():
                            print("Case diff after space: " + diff_list[i] + "/" + diff_list[i+1])
                        else:
                            print("Not case diff after space: " + diff_list[i] + "/" + diff_list[i+1])
                            case_only = False
                    elif diff_list[i][0] != ' ' and i > 0 and diff_list[i-1][0] != ' ':
                        print("Diff after diff: " + diff_list[i-1] + "/" + diff_list[i])
                    elif diff_list[i][0] != ' ' and i > 0:
                        if i+1 < len(diff_list) and diff_list[i][-1].lower() == diff_list[i+1][-1].lower():
                            print("Case diff not after space: " + diff_list[i] + "/" + diff_list[i+1])
                        else:
                            print("Not case diff not after space: " + diff_list[i] + "/" + diff_list[i+1])
                    else:
                        print("Not a diff: " + diff_list[i])
                '''
                                            
            else:
                
                if debug:
                    print("Default (" + str(len(component_set)) + ") :")
                    print(component_set)
            
                    print("No cases or spaces (" + str(len(alt_component_set)) + "):")
                    print(alt_component_set)
                    
                    print("No cases (" + str(len(component_set_caseless)) + "):")
                    print(component_set_caseless)
                
                #max_length = 0
                #for component in component_set_caseless:
                #    if len(component.split(' ')) > max_length:
                #        max_length = len(component.split(' '))
                
                
                #if len(component_set_caseless) in distribution.values:
                #    for k, value in component_set_caseless.items():
                #        pass
                  
                if len(component_set_caseless) == 2:
                
                    case_variation_alignment = {}
                    
                    for uncased_value in list(component_set_caseless):
                        for cased_value in list(component_set):
                            if uncased_value == cased_value.lower():
                                if uncased_value in case_variation_alignment.keys():
                                    case_variation_alignment[uncased_value].append(cased_value)
                                else:
                                    case_variation_alignment[uncased_value] = [cased_value]

                    #print(case_variation_alignment)
                    
                    processed_list = []
                    for grouped_list in case_variation_alignment.values():
                        if len(grouped_list) == 1:
                            processed_list.append(grouped_list[0])
                        else:
                            processed_list.append(punctuated_title(grouped_list[0]))                       
                    
                    #phrase1 = list(component_set_caseless)[0]
                    #string2 = list(component_set_caseless)[1]
                    
                    string1 = list(processed_list)[0]
                    string2 = list(processed_list)[1]
                    
                    if len(string1.split(' ')) > len(string2.split(' ')):
                        longest = string1.split(' ')
                        shortest = string2.split(' ')
                    else:
                        longest = string2.split(' ')
                        shortest = string1.split(' ')                         
                    
                    #print(longest)   
                    #print(shortest) 
                    
                    #distribution = split_part_distribution(component_list_caseless)
                    matched_value, matched_warnings = get_match_matrix(longest, shortest, component_list, debug)
                    matched_value = clean_brackets(matched_value)
                    component_set = set([matched_value])
                    warnings[key].update(matched_warnings)
                    
                    #print(component_set)
                elif len(component_set_caseless) > 2:
                    # 2025-03-14: Not implemented yet
                    print("1. WARNING! - len(component_set_caseless) > 2 in component_compare.")
                    #warnings[key].add("1. ERROR! - len(component_set_caseless) > 2 in component_compare. This code hasn't been implemented yet!")
                    print(component_set_caseless)
                    reduced_values, reduced_warnings = reduce_multiple_variations(component_list, component_set_caseless, debug)
                    combined_values[key] = reduced_values
                    
                    for reduced_warning in reduced_warnings:
                        warnings[key].add(reduced_warning)
                    
       
        #distribution = split_distribution(component_list)
        #distribution = split_part_distribution(component_list)

        if len(component_set) < 2:  # One version
            basic_join = "".join([component for component in component_set])
            if debug:
                print("Basic join - " + key + ": " + basic_join)
            combined_values[key] = basic_join
        elif len(component_set) == 2:   # Two variations
            two_phrase_join, two_phrase_join_warnings = combine_two_phrases(component_set, component_list, debug)
            #two_phrase_join = re.sub(r'(\?)?\) \(', ' ', two_phrase_join)
            #print("Two phase warnings:" + str(two_phrase_join_warnings))
            warnings[key].update(two_phrase_join_warnings)
            if debug:
                print("Two part join - " + str(key) + ": " + two_phrase_join)
                print("Component set: " + str(component_set))
                print("Component list: " + str(component_list))
            combined_values[key] = two_phrase_join
        else:   # More than two variations
            reduced_values, reduced_warnings = reduce_multiple_variations(component_list, component_set, debug)
            combined_values[key] = reduced_values
            for reduced_warning in reduced_warnings:
                warnings[key].add(reduced_warning)
    
    #print("Component compare combined values: " + str(combined_values))
    #print("Component compare warnings: " + str(warnings))
                
    return (combined_values, warnings)


def reduce_multiple_variations(component_list, component_set, debug=False):
    #print(component_set)
    warnings = set()
    warnings.add("Warning: Attempting to combine multiple (>2) variations.")
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
    
    #similar_list =[component for component in component_list if component in similar]
    #print("Similar list")
    #print(similar_list)
    #subset_distribution = split_part_distribution(similar_list)
    modified_best_similar_list = []

    while len(similar) > 1:
        if debug:
            print("reduce_multiple_variations: Option E")
            print(similar)              

        best_match = 0
        best_similar = {}
        for component1 in similar:
            for component2 in similar:
                if component1 != component2:
                    ratio = fuzz.ratio(component1, component2)   
                    if ratio > best_match:
                        best_match = ratio
                        best_similar = {component1, component2}
                        
        best_similar_list = modified_best_similar_list + [component for component in component_list if component in best_similar]
        if debug:
            print("Print calling combined phrases with:")
            print("Best similar: " + str(best_similar))
            print("Best similar list: " + str(best_similar_list))                   
        part_combined_phrases, part_sub_set_warnings = combine_two_phrases(best_similar, best_similar_list, debug)   
        #print(part_sub_set_warnings)                              
        warnings.update(part_sub_set_warnings)
        #part_combined_phrases = re.sub(r'\(+', '(', part_combined_phrases)
        #part_combined_phrases = re.sub(r'(\?\))+', '?)', part_combined_phrases)
        
        for i in range (0, len(best_similar_list)):
            modified_best_similar_list.append(part_combined_phrases)
        
        similar = similar.difference(best_similar)
        similar.add(part_combined_phrases)

    #combined_phrases = re.sub(r'(\?)?\) \(', ' ', "".join(list(similar)))
    combined_phrases = clean_brackets("".join(list(similar)))
    
    if len(distinct) > 0:
        return (combined_phrases + "/(" + "?/ ".join(distinct) + "?)", warnings)
    else:
        return (combined_phrases, warnings)


def punctuated_title(to_convert):
    ''' Converts string to punctuated title case
    
        Key argument:
            to_convert - string to be converted
        
        Returns:
            Converted string   
    '''
    
    #print(to_convert)
    lower_to_upper = re.sub(r'(\s|^)([a-z])', to_upper, to_convert)
    #print(lower_to_upper)
    converted = re.sub(r'([^\s])([A-Z])', to_lower, lower_to_upper)
    #print(upper_to_lower)
    return converted

def to_upper(match):
    ''' Convert text in the second group of a regex match object to uppercase
    
        Key Arguments:
            match - a regex match with two groups expected. The first group matches whitespace or the start of a line. The second group is subsequent lowercase text.
            
        Returns:
            String with value of first group followed by value of second group converted to uppercase.
    '''
    
    return match.group(1) + match.group(2).upper()  

def to_lower(match):
    ''' Convert text in the second group of a regex match object to lowercase
    
        Key Arguments:
            match - a regex match with two groups expected. The first group matches something that is not whitespace. The second group is subsequent uppercase text.
            
        Returns:
            String with value of first group followed by value of second group converted to lowercase.
    '''
    
    return match.group(1) + match.group(2).lower()                            
                
def ratio_check(length, ratio):
    ''' Checks similarity ratio with a sliding scale based on length of the phrase
    
        Keyword arguments:
            length - length of the phrase being tested. 
            ratio - similarity ratio
            
        Returns boolean - True if similar, False if not
    '''

    if length < 4 and ratio >= 60:
        return True
    elif length < 8 and ratio >= 70:
        return True
    elif length >= 8 and ratio >= 80:
        return True
    else:
        return False                  

def split_distribution (component_list):
    ''' Calculates the distribution of a pair of variations. (Note - not currently used. Superseded by split_part_distribution)
        
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

def token_distribution (component_list, tokens, debug=False):
    ''' Calculates the distribution of variation tokens
        
        Keyword arguments:
        component_list - list of components
        tokens - list of component tokens
        
        return a dictionary with the counts for each token in the components
    '''
    component_distribution = {}
    if debug:
        print("List: " + str(component_list))
        print("Tokens: " + str(tokens))
    
    for component in component_list:
        for token in tokens:
            if token.lower() in component.lower() and token in component_distribution.keys():
                component_distribution[token] = component_distribution[token] + 1
            elif token.lower() in component.lower():
                component_distribution[token] = 1
            
    return component_distribution        

def get_tokens (component_set):
    ''' split the components in the set into substrings and return  
    
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

def combine_connected_letters(list_to_test, string_to_compare):
    ''' Checks for multiple corrections from the same source string next to each other and combines them
    
        Keyword arguments:
            list_to_test - list of string sections to be checked
            string_to_compare - string to compare against
            
        Returns:
            List of tidied up string sections
    '''
    
    #print("String to test: " + string_to_test + " , string to compare: " + string_to_compare)    
    string_to_test = ''.join(list_to_test)
    
    replacements = re.findall(r'((\(\w+\?\))+)', string_to_test)
    if replacements:
        for match in replacements:
            group = match[0]           
            group_clean = re.sub(r'[\(\?\)]', '', group)
            
            longest_match_group = ""
            #print("match_group: " + group_clean)
            for s in range(0, len(group_clean)):
                for i in range(1, len(group_clean) + 1):
                    if i > s:
                        substr = group_clean[s:i]
                        #print("Checking: " + substr + " in " + string_to_compare)
                        if substr in string_to_compare and len(substr) > len(longest_match_group):
                            longest_match_group = substr
                            
            if len(longest_match_group) > 1:
                longest_match_group_split = re.sub(r'(\w)', r'\\(\1\\?\\)', longest_match_group)
                #print(longest_match_group_split + " in " + string_to_test)
                result = re.sub(longest_match_group_split, r'(' + longest_match_group + '?)', string_to_test)
                
                #match_results = re.findall(r'((\(\w+\?\))|(\(\?\))|(.))', result)
                #result_list = []
                #for match_result in match_results:
                #    result_list.append(match_result[0])    
                # return results_list            

                return chunk_punctuated_string(result)
                    
    
    return list_to_test                         

def chunk_punctuated_string(string_to_process, all=True):
    ''' Split the given string up on "(?)" and bracketed phrases ending in "?)" 
    
        Key Arguments:
            string_to_process - String to be split up
            all - Boolean. True by default. If True return all the sections. If False only return the sections with question marks in.
            
        Returns:
            List with the chunked parts
    
    '''
    
    match_results = re.findall(r'((\(\w+\?\))|(\(\?\))|(.))', string_to_process)
    chunked_list = []
    for match_result in match_results:
        if all:
            chunked_list.append(match_result[0]) 
        elif "?" in match_result[0]: 
            chunked_list.append(match_result[0])
        
    return chunked_list     

def combine_two_phrases(component_set, component_list, debug=False):
    ''' Combine two string phrases
    
        Key Arguments:
            component_set - Set of the component values
            component_list - List of the component values
            debug - Boolean. False by default. If True the extra debug is printed out
            
        Returns:
            A tuple with the combined phrase as a string and a set of warnings        
    '''
    
    #print(key + ": " + ", ".join([component for component in component_set]))
    #print(key + ": ")
    
    #debug = True

    split_components, count_of_component_lengths = get_tokens(component_set)
    #warnings = set()
    distribution = split_part_distribution(component_list)
    if debug:
        print("Combine_two_phrases called")
        print(split_components)
        print(count_of_component_lengths)
        print(len(count_of_component_lengths))
        print("distribution: " + str(distribution))
        
        
    aligned_phrases, phrase_warnings = align_two_phrases(split_components[0], split_components[1], component_list, debug)
    #print(key + " aligned phrases: " + str(aligned_phrases))
    return (aligned_phrases, phrase_warnings) 
    
    '''
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
                        
                    warnings.add("Note: Combining initial and names.")
                else:
                    #print("Option A")
                    generated_component += " " + combine_two_words(list(parts.keys())[0], list(parts.keys())[1], distribution, debug)
                    #print(parts)
                
            elif len(parts.keys()) < 2: # component tokens are the same
                generated_component += " " + list(parts.keys())[0]
            elif len(parts.keys()) == 2: # if there are two variations
                #print("Option B")
                generated_component += " " + combine_two_words(list(parts.keys())[0], list(parts.keys())[1], distribution, debug)
                warnings.add("Note: Combining variations.")
            else: # if there are more than two versions
                print(key + ": Option C")
                warnings.add("Note: Combining variations.")
                    
        #print(key + ": " + generated_component.strip())
        return (generated_component.strip(), warnings)
    
    else:
        
        aligned_phrases, phrase_warnings = align_two_phrases(split_components[0], split_components[1], component_list)
        if debug:
            print("Option D - Align two phrases")
            #print(split_components[0])
            #print(split_components[1])
            print(key + ": " + list(align_two_phrases(split_components[0], split_components[1], component_list, debug))[0])
            
        warnings.update(phrase_warnings)
            
        #warnings.add("Note: Combining multi-length variations.")
        return (aligned_phrases, warnings)  
'''

def combine_two_words (component1, component2, word_ratio, debug=False):
    ''' Combine two text chunks into a single chunk
    
        Keyword arguments:
        component1 - string treated as discrete chunk of text
        component2 - string treated as discrete chunk of text
        word_ratio - dictionary of variation ratio
        debug - boolean, False by default, if True print out debug
        
        returns string with combined values
    '''
    
    ratio = fuzz.ratio(component1, component2)
    ratio_caseless = fuzz.ratio(component1.lower(), component2.lower())
    ratio_caseless_no_punc = fuzz.ratio(clean_string(component1.lower()), clean_string(component2.lower()))
    warnings = set()
       
    if debug:
        print("component1: " + component1)
        print("component2: " + component2)
        print("distribution: " + str(word_ratio))
        print("ratio: " + str(ratio))
        print("ratio (caseless): " + str(ratio_caseless))
        print("ratio (caseless, no punc): " + str(ratio_caseless_no_punc))
        
    if ratio_caseless_no_punc == 100:
        
        if len(component1) > len(component2):
            return (punctuated_title(component1), warnings) 
        else:
            return (punctuated_title(component2), warnings)
    else:
        component1_count = 0
        component2_count = 0
        
        for key in word_ratio:
            if component1.lower() == key.lower():
                component1_count = word_ratio[key]
                
            if component2.lower() == key.lower():
                component2_count = word_ratio[key]
        
        #print(component1 + ": " + str(component1_count))
        #print(component2 + ": " + str(component2_count))
                    
        if component1_count > component2_count:
            generated_string_list =  component1 + " (" + component2 + "?)"
        elif component2_count > component1_count:
            generated_string_list =  component2 + " (" + component1 + "?)"
        else:
            if ratio_check(len(component1), ratio): # if the variations are similar
                component1_to_test = component1
                component2_to_test = component2
                
                if "?)" in (component1 + component2):
                    component1_to_test = re.sub(r'[\(\?\)]', '', component1)
                    component2_to_test = re.sub(r'[\(\?\)]', '', component2)

                if ratio_caseless > ratio:
                    component1_to_test = component1_to_test.lower()
                    component2_to_test = component2_to_test.lower()
                    
                    
                diff = difflib.Differ().compare(component1_to_test, component2_to_test)                 
                                   
                generated_string_list = [s.strip() if s[0] == ' ' else '(' + s[-1] + '?)' for s in diff]
                
                section_split = chunk_punctuated_string(component1 + component2, False)
                #print("Generated String: " + str(generated_string_list))
                #print("Components: " + str(section_split))
                
                for section in section_split:
                    if section not in generated_string_list:
                        #print("Section not found: " + section)
                        cleaned_section = clean_string(section)
                        
                        current_generated_string = ''.join(generated_string_list)
                        substr_count = current_generated_string.count(cleaned_section)
                        
                        #print("Substr count: " + str(substr_count))
                        # does it appear more than once in generated string?
                        # if yes then need to get context to position for positioning
                        # if no then need to insert into list in replace of the individual sections 
                        
                        if substr_count < 2:
                            #current_generated_string = re.sub(cleaned_section, section, current_generated_string)
                            
                            contexts = get_context(section, component1 + "|" + component2)
                            #print(cleaned_section)
                            #print(contexts)
                            
                            for context in contexts:
                                if section in context:
                                    context = [context[0]] + list(cleaned_section) + context[2:]
                                    
                                replacement = [context[0]] + [section] + context[len(cleaned_section)+1:]
                                
                                #print("Replacement: " + str(replacement))
                                #print("Context: " + str(context))
                                if "|" in context:
                                    context = context.remove("|")
                                
                                context_string = ''.join(context)
                                #print("context: " + context_string)
                                replacement_string = ''.join(replacement)
                                #print("replacement: " + replacement_string)
                                #print("current string: " + current_generated_string)
                                if context_string in current_generated_string:
                                    current_generated_string = current_generated_string.replace(context_string, replacement_string)
                                #print("new string: " + current_generated_string)
                                
                            generated_string_list = chunk_punctuated_string(current_generated_string)
                            
                        else:
                            contexts = get_context(section, component1 + "|" + component2)
                            
                            # 2025-03-13: Not implemented yet
                            print("2. WARNING! - substr_count is > 1 in combine_two_words. This code hasn't been implemented yet!")
                            warnings.add("2. WARNING! - substr_count is > 1 in combine_two_words. This code hasn't been implemented yet!")
                            
                            #print(cleaned_section)
                            print(contexts)
                        
                        #print("Generated string list: " + str(generated_string_list))        
                        
                
            else:            
                comp_list = [component1, component2]
                generated_string_list = "/".join(sorted(comp_list, key=str.lower)) + "(?)"        
    
    '''
    elif ratio_check(len(component1), ratio): # if the variations are similar
        #generated_component += " " + list(parts.keys())[0] + "/" + list(parts.keys())[1]
        if ratio_caseless > ratio:
            diff = difflib.Differ().compare(component1.lower(), component2.lower())
        else:
            diff = difflib.Differ().compare(component1, component2)   
        
        generated_string_list = [s.strip() if s[0] == ' ' else '(' + s[-1] + '?)' for s in diff]
    else:
        #print("Option B: " + str(ratio))
        
        component1_count = 0
        component2_count = 0
        
        for key in word_ratio:
            if component1.lower() == key.lower():
                component1_count = word_ratio[key]
                
            if component2.lower() == key.lower():
                component2_count = word_ratio[key]
        
        #print(component1 + ": " + str(component1_count))
        #print(component2 + ": " + str(component2_count))
            
        
        if component1_count > component2_count:
            generated_string_list =  component1 + " (" + component2 + "?)"
        elif component2_count > component1_count:
            generated_string_list =  component2 + " (" + component1 + "?)"
        else:
            comp_list = [component1, component2]
            generated_string_list = "/".join(sorted(comp_list, key=str.lower))
        '''    
    
    generated_string_list1 = combine_connected_letters(generated_string_list, component1)
    generated_string_list = combine_connected_letters(generated_string_list1, component2)

    generated_string = ''.join(generated_string_list)
    #print("Generated string: " + generated_string)    
    
    if ratio_caseless > ratio:
        generated_string = punctuated_title(generated_string)
        
    if debug:
        print("Generated string list: " + str(generated_string_list))
        print("Generated string 1 (compared to " + component1 + "): " + str(generated_string_list1))
        print("Generated string 2 (compared to " + component2 + "): " + str(generated_string_list))
        #print("Generated string: " + generated_string)
        
    return (generated_string, warnings)

def get_context(letter_group, phrase_string):
    ''' Finds the substring within the phrase and returns it with the immediately surrounding letters for every place it is found in the parent phrase
    
        Keyword Arguments:
            letter_group - string containing a substring of the phrase_string
            phrase_string - string with a text that contains the letter_group
            
        Returns:
            List of strings from each place in the phrase_string where the letter_group appears. These string are composed of the letter group and the proceeding and following characters.
    
    '''
    
    section_split_long = chunk_punctuated_string(phrase_string)
    #print("Chunked phrase string: " + str(section_split_long))
    context = []
    cleaned_letter_group = clean_string(letter_group)
    #print("Cleaned letter group: " + cleaned_letter_group)
    cleaned_letter_list = list(cleaned_letter_group)
    #print("Cleaned letter list: " + str(cleaned_letter_list))
    
    for i, x in enumerate(section_split_long):
        start = 0
        end = len(section_split_long)

        length_of_letters = len(cleaned_letter_list)
        if i + length_of_letters <= len(section_split_long):
            chunk_to_check = section_split_long[i:i + length_of_letters]
        else:
            chunk_to_check = section_split_long[i:]
        
        #print("Cleaned letter list: " + str(cleaned_letter_list) + ", current chunk: " + str(chunk_to_check))
        
        if x == letter_group:
            if i - 1 > 0:
                start = i - 1
            if i + 2 <= end:
                end = i + 2
            #print("Checking: " + x + ", Start:" + str(start) + ", End:" + str(end)) 
            #print("Section with context" + str(section_split_long[start:end]))      
            context.append(section_split_long[start:end])    
            
        if chunk_to_check == cleaned_letter_list:
            if i - 1 > 0:
                start = i - 1
            if i + 1 + length_of_letters <= end:
                end = i + 1 + length_of_letters
            #print("Checking: " + str(chunk_to_check) + ", Start:" + str(start) + ", End:" + str(end)) 
            #print("Section with context" + str(section_split_long[start:end]))      
            context.append(section_split_long[start:end])  
        
    return context

def align_two_phrases(string1, string2, component_list, debug=False):
    ''' Checks if two strings align and return a combined version

        Key Arguments:
            string 1 - the first phrase
            string 2 - the second phrase
            component_list - list of components
            debug - boolean, False by default, if True print out debug
        
        Returns:
            tuple with string with combined values and warnings
    '''
    if debug:
        print("align_two_phrases called with '" + str(string1) + "' & '" + str(string2) + "'" )
    
    #diff = difflib.Differ().compare(string1, string2)
    #print("\n".join(diff))
    
    #components1 = string1.split(" ")
    #components2 = string2.split(" ")
    
    combined = ""
    
    warnings = {"Note: Combining multi-length or offset variations."}
    
    if len(string1) > len(string2):
        longest = string1
        shortest = string2
    else:
        longest = string2
        shortest = string1       

    if debug:
        print("phrase1: " + str(longest))
        print("phrase2: " + str(shortest))
   
    aligned_phrase, phrase_warnings = get_match_matrix(longest, shortest, component_list, debug)
    
    warnings.update(phrase_warnings)
    
    if debug:
        print(aligned_phrase)
        
    return (aligned_phrase, warnings)

def clean_string(string_to_clean):
    ''' Remove everything except spaces and word characters
    
        Key arguments:
            string_to_clean - string to be processed
            
        Returns:
            Cleaned string
    
    '''
    return re.sub(r'[^\w\s]', '', string_to_clean)

def clean_brackets(string_to_clean):
    ''' Tidy up brackets by removing doubled additions
    
        Key Arguments:
            string_to_clean - string to tidy up
            
        Returns:
            Cleaned string   
    '''
    #print("\nClean brackets called with " + string_to_clean)
    
    string_to_clean = re.sub(r'(\?)?\) \(', ' ', string_to_clean)
    #print("String to clean before loop: " + string_to_clean) 
    while bool(re.search(r'\(\((\w+)\?\)\?\)', string_to_clean)):
        string_to_clean = re.sub(r'\(\((\w+)\?\)\?\)', r'(\1?)', string_to_clean)
        #print("String to clean in loop: " + string_to_clean) 
        
    #print("Returning: " + string_to_clean)    
        
    return string_to_clean

def initials_replace(phrase_to_be_processed, phrase_for_comparison, debug=False):
    ''' Compare two phrases. If there are any initials (single letter word when punctuation removed) in the phrase to be processed then check if they match with the first letter of the phrase for comparison then expand the initial to the matching word.
    
        Key Argument:
            phrase_to_be_processed - string to be processed
            phrase_for_comparison - string to use for comparison
            debug - boolean, False by default, if True print out debug
            
        Returns:
            Processed string
    '''
    
    if debug: 
        print("phrase_to_be_processed: " + phrase_to_be_processed)
        print("phrase_for_comparison: " + phrase_for_comparison)
    
    if True in [True for part in phrase_to_be_processed.split(' ') if len(clean_string(part)) < 2]:
        
        initials = [part for part in phrase_to_be_processed.split(' ') if len(clean_string(part)) < 2]
        
        if debug:        
            print("\nInitials: " + str(initials))
            print("Split phrase for comparison: " + str(phrase_for_comparison.split(' ')))
        
        for initial in initials:
            initial_no_punc = clean_string(initial)
            for comparison_part in phrase_for_comparison.split(' '):
                if debug: 
                    print("Comparison part: " + comparison_part)
                    
                if comparison_part != '' and initial_no_punc == comparison_part[0]:
                    phrase_to_be_processed = re.sub(r'^'+initial+r'(\s|$)', comparison_part, phrase_to_be_processed)
                    if debug: 
                        print("Processed phrase: " + phrase_to_be_processed + "\n")   
                    
    return phrase_to_be_processed

def get_match_ratios(phrase1, phrase2, debug = False):
    ''' Loops over the chunks of phrase sections of phrase1 and compares with the incrementally combined sections from phrase2 and gets the similarity ratios for each comparison. Returns the ratio for the best match (or matches) and the details of what was compared and the ratio for each comparison
    
        Key Arguments:
            phrase1 - list of phrase sections for comparison
            phrase2 - list of phrase sections for comparison
            debug - boolean, False by default, if True print out debug
            
        Returns:
            Tuple with float ratio of best match between phrase chunks and dictionary with tuple containing the section of phrase2 being compared as "phrase2 start position: 
            phrase2 end position" and the similarity ration of the phrase1 phrase chunk to the section of phrase2 with the position of the phrase1 word chunk as the key
    '''

    match_matrix = {}
    anchor_ratio = 0
    
    if debug:
        print("get_match_ratios called with phrase1: " + str(phrase1) + ", phrase2: " + str(phrase2))
    
    for i in range(0, len(phrase1)):
        max_ratio = 0
        for j1 in range(0, len(phrase2)):
            for j2 in range (j1, len(phrase2)):
                combined_string = ''.join(phrase2[j1:j2+1])
                key = str(j1) + ":" + str(j2+1)
                
                combined_string_no_punc = clean_string(combined_string)
                phrase2_no_punc = clean_string(phrase1[i])
                
                if debug:
                    print(combined_string_no_punc)
                    print(phrase2_no_punc)
                
                ratio = fuzz.ratio(phrase2_no_punc.lower(), combined_string_no_punc.lower())
                
                if debug: 
                    combo = "A" + str(i) + "-B" + ": " + str(j1) + "-" + str(j2) + " (" + phrase2[i].lower() + "-" + combined_string.lower() +  ") = " + str(ratio)
                    print(combo)
                    
                if ratio > max_ratio:
                    match_matrix[i] = (key, ratio)
                    max_ratio = ratio
                    
                if ratio >= anchor_ratio:
                    anchor_ratio = ratio  
                    
    return (anchor_ratio, match_matrix)

def get_match_matrix(first_phrase, second_phrase, component_list, debug=False):
    ''' get the comparison matrix
    
        keyword arguments:
        phrase1 - the first list
        phrase2 - the second list
        word_ratio - dictionary of variation ratio
        debug - boolean, False by default, if True print out debug
        
        return tuple with string containing combined values and warnings
    '''
    #debug = True
    if debug:
        print("Match matrix called with " + str(first_phrase) + " and " + str(second_phrase))
    match_warnings = set()
    
    #match_matrix_by_phrase2 = {}
    match_matrix_by_phrase1 = {}
    #print(phrase1)
    #print(phrase2)
    
    #for i in range(0, len(phrase1)):
    #    match_matrix_by_phrase2[i] = {j: fuzz.ratio(phrase1[i], phrase2[j]) for j in range(0, len(phrase2))}
    
    #print("Form each in phrase1:")
    #print(match_matrix_by_phrase2)
    
    # by default, phrase1 should be shorter or the same length as phrase2
    if len(first_phrase) > len(second_phrase):
        phrase1 = second_phrase
        phrase2 = first_phrase
    else:
        phrase1 = first_phrase
        phrase2 = second_phrase     
    
    
    
    anchor_ratio, match_matrix_by_phrase1 = get_match_ratios(phrase1, phrase2, debug)    
    #anchor_ratio_by_phrase2, match_matrix_by_phrase2 = get_match_ratios(phrase2, phrase1, debug)  
              

    if debug:
        print("For each in phrase1 (" + str(phrase1) + "):")        
        print(match_matrix_by_phrase1)
        #print("For each in phrase2:")        
        #print(match_matrix_by_phrase2)
    
    best_anchor_points = []
    
    last_position_phrase2 = 0
    last_position_phrase1 = 0
    
    for phrase1_position, phrase2_details in match_matrix_by_phrase1.items():
        phrase2_position, best_ratio = phrase2_details
        phrase2_start = int(phrase2_position.split(":")[0])
        phrase2_end = int(phrase2_position.split(":")[1])  
        if debug:
            print("phrase1 position: " + str(phrase1_position))
            print("phrase2 position: " + str(phrase2_position))
            print("phrase2 start: " + str(phrase2_start))
            print("phrase2 end: " + str(phrase2_end))
            print("best ratio: " + str(best_ratio))
            
         
        
        # make list of anchor points (points with highest match ratio)
        if best_ratio == anchor_ratio:
            if phrase1_position >= last_position_phrase1 and phrase2_end >= last_position_phrase2:
                last_position_phrase1 = phrase1_position
                last_position_phrase2 = phrase2_end                
                best_anchor_points.append((phrase1_position, phrase2_position))
                
    if debug:
        print("Best anchor ratio: " + str(anchor_ratio))
        #print(str(anchor_ratio_by_phrase2))
        print("Best anchor points:" + str(best_anchor_points))
        for anchor_points in best_anchor_points:
            phrase1_start, phrase2_range = anchor_points
            phrase2_start = int(phrase2_range.split(":")[0])
            phrase2_end = int(phrase2_range.split(":")[1])   
            print("Anchor point - " + str(phrase1_start) + ": " + str(phrase1[phrase1_start]) + "/" + str(phrase2_start) + "-" + str(phrase2_end) + ": " + ' '.join(phrase2[int(phrase2_start):int(phrase2_end)])) 
        
        #print("phrase1: " + str(phrase1) + ",  length: " + str(len("".join(phrase1))))
        #print("phrase2: " + str(phrase2) + ",  length: " + str(len("".join(phrase2))))
    
    #check if passes the ratio check given the length of the string
    if ratio_check(len("".join(phrase1)), anchor_ratio):
        anchored_list = []
        phrase1_pointer = 0
        phrase2_pointer = 0
        last_phrase2_anchored_point = 0
        
        for anchor_points in best_anchor_points:
            phrase1_start, phrase2_range = anchor_points
            phrase2_start = int(phrase2_range.split(":")[0])
            phrase2_end = int(phrase2_range.split(":")[1])
            phrase1_token = ""
            phrase2_token = ""
            last_phrase2_anchored_point = phrase2_end
            
            # while Phrase1 pointer is pointing at or before the phrase1 start and the Phrase2 pointer has not reached the end of the phrase2 values
            while phrase1_pointer <= phrase1_start and phrase2_pointer <= phrase2_end:
                if debug:
                    print("Before - Phrase1 pointer: " + str(phrase1_pointer) + ", phrase1 start: " + str(phrase1_start)) 
                    print("Before - Phrase2 pointer: " + str(phrase2_pointer) + ", phrase2 start: " + str(phrase2_start)) 
                
                # if phrase1 is at start but phrase2 is before the first start point
                if phrase1_pointer == phrase1_start and phrase2_pointer < phrase2_start:
                    phrase2_token = ' '.join(phrase2[phrase2_pointer:phrase2_start])
                    
                    if len(anchored_list) > 0 and phrase2_pointer > 0:
                        if debug: 
                            print("Anchored List: " + str(anchored_list[-1]))
                            print("Previous token: " + str(phrase2[phrase2_pointer - 1]))
                            print("New token: " + str(phrase2_token))
                        
                        # if the end of the last thing added to the anchored list is a comma, the end of the previous phrase2 section wasn't a comma and the end of the current section is a comma
                        try:
                            if str(anchored_list[-1])[-1] == "," and str(phrase2[phrase2_pointer - 1])[-1] != "," and phrase2_token[-1] == ",":
                                anchored_list[-1] = str(anchored_list[-1])[:-1]
                                phrase2_token = phrase2_token[:-1]
                                anchored_list.append("(" + phrase2_token + "?),")
                            else:
                                anchored_list.append("(" + phrase2_token + "?)")
                        except Exception as e:
                            print("Anchored List: " + str(anchored_list[-1]))
                            print("Previous token: " + str(phrase2[phrase2_pointer - 1]))
                            print("New token: " + str(phrase2_token))
                           
                    phrase2_pointer = phrase2_start
                    
                    if debug:
                        print("Added 'phrase2' string to bring into alignment")
                        print("Adding (phrase2): " + phrase2_token + " from " + str(phrase2))
                        print("Phrase2 pointer: " + str(phrase2_pointer))
                        
                # if pointer is before phrase1 start but phrase2 is at start point        
                elif phrase1_pointer < phrase1_start and phrase2_start == phrase2_pointer:
                    phrase1_token = phrase1[phrase1_pointer]
                    
                    if len(anchored_list) > 0 and phrase1_pointer > 0:
                        if debug: 
                            print("Anchored List: " + str(anchored_list[-1]))
                            print("Previous token: " + str(phrase1[phrase1_pointer - 1]))
                            print("New token: " + str(phrase1_token))
                        
                        if str(anchored_list[-1])[-1] == "," and str(phrase1[phrase1_pointer - 1])[-1] != "," and phrase1_token[-1] == ",":
                            anchored_list[-1] = str(anchored_list[-1])[:-1]
                            phrase1_token = phrase1_token[:-1]
                            anchored_list.append("(" + phrase1_token + "?),")
                        else:
                           anchored_list.append("(" + phrase1_token + "?)")                    

                    phrase1_pointer += 1
                    
                    if debug:
                        print("Added 'phrase1' string to bring into alignment")
                        print("Adding (phrase1): " + phrase1_token + " from " + str(phrase1))
                        print("Phrase1 pointer: " + str(phrase1_pointer))
                
                # if pointers for both phrase1 and phrase2 are at their respective start points        
                elif phrase2_start == phrase2_pointer and phrase1_start == phrase1_pointer:
                    phrase1_token = phrase1[phrase1_start] 
                    phrase2_token = ' '.join(phrase2[int(phrase2_start):int(phrase2_end)])                        
                    
                    if phrase2_token != phrase1_token:
                        token_ratio = token_distribution(component_list, [phrase1_token, phrase2_token], debug)
                        #print("Combine two words called from match_matrix_by_phrase2 (pointers matched) with " + phrase1_token + " and " + phrase2_token)
                        
                        combined_token, combination_warnings = combine_two_words(phrase1_token, phrase2_token, token_ratio, debug)
                        match_warnings.update(combination_warnings)

                        if debug:
                            print("Added combined section")
                            print("phrase1 token: " + phrase1_token)
                            print("phrase2 token: " + phrase2_token)
                            print("Token ratio: " + str(token_ratio))
                            print("Adding (combined match): " + combined_token)
                    else:
                        combined_token = phrase1_token
                        
                    anchored_list.append(combined_token)
                    phrase2_pointer = phrase2_end
                    phrase1_pointer += 1
                    
                # if pointers for both phrase1 and phrase2 are before their respective start points     
                else:
                    phrase1_token = ' '.join(phrase1[phrase1_pointer:phrase1_start])
                    phrase2_token = ' '.join(phrase2[int(phrase2_pointer):int(phrase2_start)])
                    phrase1_pointer = phrase1_start
                    phrase2_pointer = phrase2_start
                    
                    phrase2_token = initials_replace(phrase2_token.strip(), phrase1_token.strip(), debug) 
                    phrase1_token = initials_replace(phrase1_token.strip(), phrase2_token.strip(), debug)                                     
                    
                    token_ratio = token_distribution(component_list, [phrase2_token, phrase1_token], debug)
                    #print("Combine two words called from match_matrix_by_phrase2 (both pointers phrase2) with " + phrase1_token + " and " + phrase2_token)
                    combined_token, combination_warnings = combine_two_words(phrase1_token, phrase2_token, token_ratio, debug)
                    match_warnings.update(combination_warnings)
                    
                    anchored_list.append(combined_token)
                    
                    if debug:
                        print("Adding combined starting string")
                        print("phrase2 token: " + phrase2_token)
                        print("phrase1 token: " + phrase1_token)
                        print("Token ratio: " + str(token_ratio))
                        print("Adding (combined gap): " + combined_token)
                                    
                if debug:
                    print("After - phrase1: " + phrase1_token + ", phrase1 pointer: " + str(phrase1_pointer) + ", phrase1 start: " + str(phrase1_start) + ", phrase1 length: " + str(len(phrase1)))
                    print("After - phrase2: " + phrase2_token + ", phrase2 pointer: " + str(phrase2_pointer) + ", phrase2 start: " + str(phrase2_start) + ", phrase2 last anchor: " + str(last_phrase2_anchored_point))
                                     
        
        if len(phrase2) > last_phrase2_anchored_point or len(phrase1) > phrase1_pointer:
            phrase1_end_token = ' '.join(phrase1[phrase1_pointer:])
            phrase2_end_token = ' '.join(phrase2[int(phrase2_end):])  
            
            phrase2_end_token = initials_replace(phrase2_end_token.strip(), phrase1_end_token.strip(), debug) 
            phrase1_end_token = initials_replace(phrase1_end_token.strip(), phrase2_end_token.strip(), debug)  
            
            component_list = [phrase2_end_token, phrase1_end_token]                              
                    
            end_token_ratio = token_distribution(component_list, [phrase2_end_token, phrase1_end_token], debug)
            
            if debug:
                print("Adding end section")
                print("Phrase2 pointer: " + str(phrase2_pointer) + ", phrase2 end: " + str(len(phrase2))) 
                print("Phrase1 pointer: " + str(phrase1_pointer) + ", phrase1 end: " + str(len(phrase1))) 
                print("component list: " + str(component_list))
                print("End token (phrase1): " + phrase1_end_token)
                print("End token (phrase2): " + phrase2_end_token)
            
            if phrase2_pointer == len(phrase2):
                #print("Phrase2 pointer at end - adding end text from phrase1")
                anchored_list.append("(" + phrase1_end_token + "?)")
            elif phrase1_pointer == len(phrase1):
                #print("Phrase1 pointer at end - adding end text from phrase2")
                anchored_list.append("(" + phrase2_end_token + "?)")
            else:
                if " " in phrase1_end_token or " " in phrase2_end_token:
                    end_phrase_join, end_phrase_join_warnings = combine_two_phrases(set(component_list), component_list, debug)
                    #print("End phrase join: " + str(end_phrase_join))
                    match_warnings.update(end_phrase_join_warnings)
                    anchored_list.append(end_phrase_join)
                else:
                    combined_token, combination_warnings = combine_two_words(phrase1_end_token, phrase2_end_token, end_token_ratio, debug)
                    #print("Combined token: " + str(combined_token))
                    anchored_list.append(combined_token)
                    match_warnings.update(combination_warnings)


        
        if debug:
            print(anchored_list)        
        
    else:
        match_warnings.add("Could not find any strong anchor points. '" + " ".join(phrase2) + "' and '" + " ".join(phrase1) + "' appear to be distinct values.")
        anchored_list = phrase2 + ["/"] + phrase1 
        
    '''
    combined = []
    
    checking = True
    x = 0
    y = 0
    
    while x < len(shortest) and checking: 
        #best_match_ratio = max(match_matrix[i].values())
        #number_of_best_matches = list(match_matrix[i].values()).count(best_match_ratio)   
        #print("x:" + str(x))
        #print("y:" + str(y))
        #print("longest:" + str(len(longest)))
        
        sorted_options = dict(sorted(match_matrix2[x].items(), key=lambda item: item[1], reverse=True))        
        
        #print("Sorted:")
        #print(sorted_options)
        best_match_ratio = max(list(sorted_options.values()))
        
        if best_match_ratio < 1: # there is no match
            combined.append("(" + longest[x] + ")")
            
            if x <= len(longest):
                x += 1                       
        else:
            best_match_longest = longest[x]
            
            not_assigned = True
            m = 0            
            #while not_assigned and m < len(shortest):
            #    if list(sorted_options.keys())[m] > y:   
            #        y = list(sorted_options.keys())[0]
            #        not_assigned = False
            #    else:
            #        m += 1
                    
            best_match_shortest = shortest[y]
            
            #print(best_match_longest[0])
            #print(best_match_shortest[0])
            
            combined.append(combine_two_words(best_match_longest, best_match_shortest, word_ratio))
            
            if x <= len(longest):
                x += 1
            
            #print("x:" + str(x) + " / " + str(len(longest)))         
            #print(combined) 
            
            #print("x:" + str(x) + " / " + str(len(longest)))      
            #print(combined) 

    if debug:
        print(combined)  
     '''       
        
    return (' '.join(anchored_list), match_warnings)
        
    #print(match_matrix)
  
        


names1 = {"1":["H Arkell", "H Arkell", "H Arkell", "H Arkell"], 
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
         "33":["F Thomas", "Frank Thomas", "F. Thomas", "Frank Thomas"]
         }

names2 = {"1": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
         "2": ["R Burroughs", "R Burroughs", "R Burroughs", "R Burroughs"],
         "3": ["R Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
         "4": ["R Burroughs", "J Burroghs", "J Burroughs", "R Burroughs"], 
         "5": ["R J Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"],
         "6": ["J R Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"], 
         "7": ["J R Burrows", "J Burroughs", "J Burroughs", "J Burroughs"], 
         "8": ["R J Burroughs", "R L Burroughs", "R Burroughs", "R Burroughs"],
         "9": ["R J Burrows", "R L Burroughs", "J Burroughs", "J Burroughs"],
         "10": ["R J Burrows", "R L Burroughs", "R Burroughs", "R Burroughs"],
         "11": ["R Burrows", "R Burroughs", "R Burroughs", "F Rymer"],
         "12": ["R Burrows", "R Burroughs", "R Burroughs", "R Rymer"],
         "13": ["R Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
         "14": ["R Burrows", "R F Burroughs", "R Burroughs", "F Rymer"],
         "15": ["R J Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
         "16": ["R J Burrows", "R Burroughs", "R Burroughs", "R J Burroghs"],
         "17": ["R J Burrows", "A E Cook", "G P Rymer", "Geo Wilkin"],
         "18": ["R J Burrows", "R Burroughs", "G P Rymer", "Geo Wilkin"],
         "19": ["R J Burrows", "R Burroughs", "R Burroghs", "R J Burroghs"],
         "20": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"]                
        }

names3 = {"1": ["Messrs Rowe and Raddy", "Mr A C Raddy for Rowe and Raddy"]}


address = {#"1":["Butlers Court Farm, Boddington, Gloucestershire", "Butlers Court, Boddington, Near Cheltenham", "Butlers Court, Boddington", "Butlers Court Farm, Boddington, Gloucestershire"], 
         #"2":["Whitehall, Hayden Hill, Cheltenham, Gloucestershire", "Whitehall Farm, Hayden, Cheltenham", "Whitehall Farm, Hayden, Cheltenham", "Whitehall, Hayden Hill, Cheltenham, Gloucestershire"], 
         "3":["Boddington House Farm, Boddington, Gloucestershire", "Boddington House Farm, Boddington, Cheltenham", "Boddington House Farm, Near Cheltenham", "Boddington House, Boddington, Gloucestershire"],
         #"6":["Slate Mill, Boddington, Near Cheltenham, Gloucestershire","Slade Mill, Boddington, Cheltenham", "Slate Mill, Boddington", "Slate Mill, Boddington, Near Cheltenham, Gloucestershire"],
         #"7":["Barrow Court, Boddington, Cheltenham, Gloucestershire", "14, Foregate Street, Worcester", "Barrow Court, Boddington", "Barrow Court, Boddington, Cheltenham, Gloucestershire"],
         #"9":["Manor Farm, Boddington, Near Cheltenham, Gloucestershire", "Guiting House, Temple Guiting, Gloucestershire", "Manor Farm, Boddington", "Manor Farm, Boddington, Near Cheltenham, Gloucestershire"],
         #"10":["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "192 High Street, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
         #"14":["14 Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, Charlton Kings, Cheltenham", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
         #"15":["Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire", "Mill House Farm, Boddington, Near Cheltenham", "Withybridge Farm, Boddington", "Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire"],
         #"16":["Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire", "Barrow Hill Farm, Boddington, Cheltenham", "Barrow Hill Farm, Boddington", "Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire"],
         #"18":["Brookes Laymes Farm, Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Brookes Laymes Farm, Boddington", "Brookes Laymes Farm, Boddington, Gloucestershire"],
         #"19":["Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Boddington", "Boddington, Gloucestershire"],
         #"20":["Hayden Farm, Boddington, Near Cheltenham, Gloucestershire", "Hayden Farm, Hayden, Cheltenham", "Hayden Farm, Boddington", "Hayden Farm, Boddington, Near Cheltenham, Gloucestershire"],
         #"22":["Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire", "Wilkins Farm, Boddington, Cheltenham", "Wilkins Farm, Barrow, Boddington", "Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire"],
         #"31":["1 Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire", "1 Hayden Hill Villas, Hayden Hill, Boddington", "Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire"],
         #"33":["Pilgrove, Hayden Hill, Near Cheltenham, Gloucestershire", "Pilgrove, Hayden Hill, Boddington, Gloucestershire", "Pilgrove, Hayden Hill, Cheltenham", "Pilgrove, Hayden Hilll, Near Cheltenham, Gloucestershire"]
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

test = {"1":["Hill Top Farm", "Hilltop farm", "Hill top farm"],
        "2": ["Hill Top Farm", "Hilltop farm", "Hilltop farm"],
        "3": ["Hill Top Farm", "Hill top farm", "Hill Top farm"],
        "4": ["Hill Top Farm", "Hilltop farm"],
        "5": ["HillTop Farm", "Hilltop farm"]}

test2 = {"1": ["Winstall Farm, South Normanton, Alfreton, Derbyshire", "South Normanton, near Alfreton, Derbyshire", "Winstall Farm, South Normanton, Alfreton, Derbyshire"]}

test3 = {"1": ["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
         "2": ["14, Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, London Road, Charlton Kings"],
         "3": ["14, Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
         "4": ['Parkside, Frizington, Cumberland', 'Parkside Farm, Frizington', 'Parkside, Frizington, Cumberland']
        }

#print(component_compare(names1))
#print(component_compare(names2))
#print(component_compare(names3))
#print(component_compare(address))
#print(component_compare(farm_name))
#print(component_compare(test))
#print(component_compare(test2))
#print(component_compare(test3))

#punctuated_title("fiNd o(u)t")