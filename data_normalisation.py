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
#   component_compare (values_to_check)
#   reduce_multiple_variations(component_list, component_set)
#   punctuated_title(to_convert)
#   to_upper(match)
#   to_lower(match)
#   ratio_check(length, ratio)
#   split_distribution (component_list)
#   split_part_distribution (component_list)
#   token_distribution (component_list, tokens)
#   get_tokens (component_set)
#   combine_connected_letters(list_to_test, string_to_compare)
#   chunk_punctuated_string(string_to_process, all=True)
#   combine_two_phrases(component_set, component_list)
#   combine_two_words (component1, component2, word_ratio)
#   get_context(letter_group, phrase_string)
#   align_two_phrases(string1, string2, component_list)
#   clean_string(string_to_clean)
#   clean_brackets(string_to_clean)
#   initials_replace(phrase_to_be_processed, phrase_for_comparison)
#   get_match_ratios(phrase1, phrase2 = False)
#   get_match_matrix(first_phrase, second_phrase, component_list)

#####################
#   To Do:
#   
#   
#   Need to do more testing with phrases espec. of different lengths - maybe do need to do the check merging both ways
#   See if there is a better way to check mismatches based on match level of chunks since addresses with extra information are incorrectly identified as a mismatch.
#   In combine_two_words - code for the case 'substr_count is > 1' hasn't been implemented

from rapidfuzz import fuzz
import difflib, re
import itertools


def component_compare (values_to_check: dict) -> tuple[dict, dict]:
    ''' Function to compare the components
    
        Keyword arguments:
        values_to_check - a dictionary of values made up of a key and a list of components
        
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
                
                #Assumption: Case mismatch - convert to title case.
                component_set = {punctuated_title(item) for item in component_set}
                
            else:
                if len(component_set_caseless) == 2:
                
                    case_variation_alignment = {}
                    
                    for uncased_value in list(component_set_caseless):
                        for cased_value in list(component_set):
                            if uncased_value == cased_value.lower():
                                if uncased_value in case_variation_alignment.keys():
                                    case_variation_alignment[uncased_value].append(cased_value)
                                else:
                                    case_variation_alignment[uncased_value] = [cased_value]

                    processed_list = []
                    for grouped_list in case_variation_alignment.values():
                        if len(grouped_list) == 1:
                            processed_list.append(grouped_list[0])
                        else:
                            processed_list.append(punctuated_title(grouped_list[0]))                       
                    
                    string1 = list(processed_list)[0]
                    string2 = list(processed_list)[1]
                    
                    if len(string1.split(' ')) > len(string2.split(' ')):
                        longest = string1.split(' ')
                        shortest = string2.split(' ')
                    else:
                        longest = string2.split(' ')
                        shortest = string1.split(' ')                         
                    
                    matched_value, matched_warnings = get_match_matrix(longest, shortest, component_list)
                    matched_value = clean_brackets(matched_value)
                    component_set = set([matched_value])
                    warnings[key].update(matched_warnings)
                    
                elif len(component_set_caseless) > 2:
                    # 2025-03-14: Not implemented yet
                    reduced_values, reduced_warnings = reduce_multiple_variations(component_list, component_set_caseless)
                    combined_values[key] = reduced_values
                    
                    for reduced_warning in reduced_warnings:
                        warnings[key].add(reduced_warning)
                    
        if len(component_set) < 2:  # One version
            basic_join = "".join([component for component in component_set])
            combined_values[key] = basic_join

        elif len(component_set) == 2:   # Two variations
            two_phrase_join, two_phrase_join_warnings = combine_two_phrases(component_set, component_list)
            warnings[key].update(two_phrase_join_warnings)
            combined_values[key] = two_phrase_join

        else:   # More than two variations
            reduced_values, reduced_warnings = reduce_multiple_variations(component_list, component_set)
            combined_values[key] = reduced_values
            for reduced_warning in reduced_warnings:
                warnings[key].add(reduced_warning)
    
    return (combined_values, warnings)


def reduce_multiple_variations(component_list: list, component_set: set) -> tuple[str, set]:
    ''' Function to deal with combine the best matches and reduce the variations down to a final string
    
        Keyword arguments:
        component_list - a list of variations original values
        component_set - a set of the variations, these may have been processed to remove case
        
        Returns    
            Tuple containing string with the combined value and a set of warnings

    '''
    
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
        
        if max_ratio < 50:
            distinct.append(component1) 
            
    similar = component_set - set(distinct)
    
    modified_best_similar_list = []

    while len(similar) > 1:
        best_match = 0
        best_similar = {}

        for (component1, component2) in itertools.combinations(similar, 2):
            ratio = fuzz.ratio(component1, component2)   
            if ratio > best_match:
                best_match = ratio
                best_similar = {component1, component2}

        if best_similar:                
            best_similar_list = modified_best_similar_list + [component for component in component_list if component in best_similar]
        else:
            best_similar = component_set
            best_similar_list = component_list

        part_combined_phrases, part_sub_set_warnings = combine_two_phrases(best_similar, best_similar_list)   
        warnings.update(part_sub_set_warnings)
        
        for i in range (0, len(best_similar_list)):
            modified_best_similar_list.append(part_combined_phrases)
        
        similar = similar.difference(best_similar)
        similar.add(part_combined_phrases)

    combined_phrases = clean_brackets("".join(list(similar)))
    
    if len(distinct) > 0:
        return (f"{combined_phrases}/({'?/ '.join(distinct)}?)", warnings)
    else:
        return (combined_phrases, warnings)


def punctuated_title(to_convert: str) -> str:
    ''' Converts string to punctuated title case
    
        Key argument:
            to_convert - string to be converted
        
        Returns:
            Converted string   
    '''
    
    lower_to_upper = re.sub(r'(\s|^)([a-z])', to_upper, to_convert)
    converted = re.sub(r'([^\s])([A-Z])', to_lower, lower_to_upper)
    return converted


def to_upper(match: re.Match) -> str:
    ''' Convert text in the second group of a regex match object to uppercase
    
        Key Arguments:
            match - a regex match with two groups expected. The first group matches whitespace or the start of a line. The second group is subsequent lowercase text.
            
        Returns:
            String with value of first group followed by value of second group converted to uppercase.
    '''
    
    return match.group(1) + match.group(2).upper()  


def to_lower(match: re.Match) -> str:
    ''' Convert text in the second group of a regex match object to lowercase
    
        Key Arguments:
            match - a regex match with two groups expected. The first group matches something that is not whitespace. The second group is subsequent uppercase text.
            
        Returns:
            String with value of first group followed by value of second group converted to lowercase.
    '''
    
    return match.group(1) + match.group(2).lower()                            


def ratio_check(length: int, ratio: float) -> bool:
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


def split_distribution (component_list: list) -> dict:
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


def split_part_distribution (component_list: list) -> dict:
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
                           
    return component_distribution


def token_distribution (component_list: list, tokens: list) -> dict:
    ''' Calculates the distribution of variation tokens
        
        Keyword arguments:
        component_list - list of components
        tokens - list of component tokens
        
        return a dictionary with the counts for each token in the components
    '''
    component_distribution = {}
    for component in component_list:
        for token in tokens:
            if token.lower() in component.lower() and token in component_distribution.keys():
                component_distribution[token] = component_distribution[token] + 1
            elif token.lower() in component.lower():
                component_distribution[token] = 1
            
    return component_distribution        


def get_tokens (component_set: set) -> tuple[list, list]:
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


def combine_connected_letters(list_to_test: list, string_to_compare: str) -> list:
    ''' Checks for multiple corrections from the same source string next to each other and combines them
    
        Keyword arguments:
            list_to_test - list of string sections to be checked
            string_to_compare - string to compare against
            
        Returns:
            List of tidied up string sections
    '''
    
    string_to_test = ''.join(list_to_test)
    
    replacements = re.findall(r'((\(\w+\?\))+)', string_to_test)
    if replacements:
        for match in replacements:
            group = match[0]           
            group_clean = re.sub(r'[\(\?\)]', '', group)
            
            longest_match_group = ""
            for s in range(0, len(group_clean)):
                for i in range(1, len(group_clean) + 1):
                    if i > s:
                        substr = group_clean[s:i]
                        if substr in string_to_compare and len(substr) > len(longest_match_group):
                            longest_match_group = substr
                            
            if len(longest_match_group) > 1:
                longest_match_group_split = re.sub(r'(\w)', r'\\(\1\\?\\)', longest_match_group)
                result = re.sub(longest_match_group_split, fr"'('{longest_match_group}'?)'", string_to_test)

                return chunk_punctuated_string(result)                   
    
    return list_to_test                         


def chunk_punctuated_string(string_to_process: str, all=True) -> list:
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


def combine_two_phrases(component_set: set, component_list: list) -> tuple[str, set]:
    ''' Combine two string phrases
    
        Key Arguments:
            component_set - Set of the component values
            component_list - List of the component values
            
        Returns:
            A tuple with the combined phrase as a string and a set of warnings        
    '''
    
    split_components, count_of_component_lengths = get_tokens(component_set)       
    aligned_phrases, phrase_warnings = align_two_phrases(split_components[0], split_components[1], component_list)

    return (aligned_phrases, phrase_warnings) 


def combine_two_words (component1: str, component2: str, word_ratio: dict) -> tuple[str, set]:
    ''' Combine two text chunks into a single chunk
    
        Keyword arguments:
        component1 - string treated as discrete chunk of text
        component2 - string treated as discrete chunk of text
        word_ratio - dictionary of variation ratio
        
        returns string with combined values
    '''
    
    ratio = fuzz.ratio(component1, component2)
    ratio_caseless = fuzz.ratio(component1.lower(), component2.lower())
    ratio_caseless_no_punc = fuzz.ratio(clean_string(component1.lower()), clean_string(component2.lower()))
    warnings = set()
       
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
                    
        if component1_count > component2_count:
            generated_string_list =  f"{component1} ({component2}?)"
        elif component2_count > component1_count:
            generated_string_list =  f"{component2} ({component1}?)"
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
                
                section_split = chunk_punctuated_string(f"{component1}{component2}", False)
                
                for section in section_split:
                    if section not in generated_string_list:
                        cleaned_section = clean_string(section)
                        
                        current_generated_string = ''.join(generated_string_list)
                        substr_count = current_generated_string.count(cleaned_section)
                        
                        # does it appear more than once in generated string?
                        # if yes then need to get context to position for positioning
                        # if no then need to insert into list in replace of the individual sections 
                        if len(cleaned_section) > 0: 
                            if substr_count < 2:
                                
                                contexts = get_context(section, f"{component1}|{component2}")
                                
                                for context in contexts:
                                    if section in context:
                                        context = [context[0]] + list(cleaned_section) + context[2:]
                                        
                                    replacement = [context[0]] + [section] + context[len(cleaned_section)+1:]
                                    
                                    if "|" in context:
                                        context.remove("|")                                    
                                    
                                    context_string = ''.join(context)
                                    replacement_string = ''.join(replacement)
                                    if context_string in current_generated_string:
                                        current_generated_string = current_generated_string.replace(context_string, replacement_string)
                                    
                                generated_string_list = chunk_punctuated_string(current_generated_string)
                                
                            else:
                                contexts = get_context(section, f"{component1}|{component2}")
                                
                                # 2025-03-13: Not implemented yet
                                print("2. WARNING! - substr_count is > 1 in combine_two_words. This code hasn't been implemented yet!")
                                warnings.add("2. WARNING! - substr_count is > 1 in combine_two_words. This code hasn't been implemented yet!")
                                
                                print(f"{cleaned_section=}")
                                print(f"{section=}")
                                print(f"{contexts=}")
                                print(f"{component1=}")
                                print(f"{component2=}")
                                print(f"{substr_count=}")
                                print(f"{generated_string_list=}")

            else:            
                comp_list = [component1, component2]
                generated_string_list = f"{'/'.join(sorted(comp_list, key=str.lower))}(?)"
    
    generated_string_list1 = combine_connected_letters(generated_string_list, component1)
    generated_string_list = combine_connected_letters(generated_string_list1, component2)

    generated_string = ''.join(generated_string_list)
    
    if ratio_caseless > ratio:
        generated_string = punctuated_title(generated_string)
        
    return (generated_string, warnings)


def get_context(letter_group: str, phrase_string: str) -> list:
    ''' Finds the substring within the phrase and returns it with the immediately surrounding letters for every place it is found in the parent phrase
    
        Keyword Arguments:
            letter_group - string containing a substring of the phrase_string
            phrase_string - string with a text that contains the letter_group
            
        Returns:
            List of strings from each place in the phrase_string where the letter_group appears. These string are composed of the letter group and the proceeding and following characters.
    
    '''
    
    section_split_long = chunk_punctuated_string(phrase_string)
    context = []
    cleaned_letter_group = clean_string(letter_group)
    cleaned_letter_list = list(cleaned_letter_group)
    
    for i, x in enumerate(section_split_long):
        start = 0
        end = len(section_split_long)

        length_of_letters = len(cleaned_letter_list)
        if i + length_of_letters <= len(section_split_long):
            chunk_to_check = section_split_long[i:i + length_of_letters]
        else:
            chunk_to_check = section_split_long[i:]
               
        if x == letter_group:
            if i - 1 > 0:
                start = i - 1
            if i + 2 <= end:
                end = i + 2
            context.append(section_split_long[start:end])    
            
        if chunk_to_check == cleaned_letter_list:
            if i - 1 > 0:
                start = i - 1
            if i + 1 + length_of_letters <= end:
                end = i + 1 + length_of_letters
            context.append(section_split_long[start:end])  
        
    return context


def align_two_phrases(string1: str, string2: str, component_list: list) -> tuple[str, set]:
    ''' Checks if two strings align and return a combined version

        Key Arguments:
            string 1 - the first phrase
            string 2 - the second phrase
            component_list - list of components
        
        Returns:
            tuple with string with combined values and warnings
    '''
    warnings = {"Note: Combining multi-length or offset variations."}
    
    if len(string1) > len(string2):
        longest = string1
        shortest = string2
    else:
        longest = string2
        shortest = string1       
   
    aligned_phrase, phrase_warnings = get_match_matrix(longest, shortest, component_list)
    
    warnings.update(phrase_warnings)
        
    return (aligned_phrase, warnings)


def clean_string(string_to_clean: str) -> str:
    ''' Remove everything except spaces and word characters
    
        Key arguments:
            string_to_clean - string to be processed
            
        Returns:
            Cleaned string
    
    '''
    return re.sub(r'[^\w\s]', '', string_to_clean)


def clean_brackets(string_to_clean: str) -> str:
    ''' Tidy up brackets by removing doubled additions
    
        Key Arguments:
            string_to_clean - string to tidy up
            
        Returns:
            Cleaned string   
    '''
    
    string_to_clean = re.sub(r'(\?)?\) \(', ' ', string_to_clean)
    while bool(re.search(r'\(\((\w+)\?\)\?\)', string_to_clean)):
        string_to_clean = re.sub(r'\(\((\w+)\?\)\?\)', r'(\1?)', string_to_clean)
        
    return string_to_clean


def initials_replace(phrase_to_be_processed: str, phrase_for_comparison: str) -> str:
    ''' Compare two phrases. If there are any initials (single letter word when punctuation removed) in the phrase to be processed then check if they match with the first letter of the phrase for comparison then expand the initial to the matching word.
    
        Key Argument:
            phrase_to_be_processed - string to be processed
            phrase_for_comparison - string to use for comparison
            
        Returns:
            Processed string
    '''
    
    if True in [True for part in phrase_to_be_processed.split(' ') if len(clean_string(part)) < 2]:
        
        initials = [part for part in phrase_to_be_processed.split(' ') if len(clean_string(part)) < 2]
        for initial in initials:
            initial_no_punc = clean_string(initial)
            for comparison_part in phrase_for_comparison.split(' '):
                if comparison_part != '' and initial_no_punc == comparison_part[0]:
                    try:                        
                        phrase_to_be_processed = re.sub(fr"""^({re.escape(initial)})\s""", f"{comparison_part} ", phrase_to_be_processed)
                    except Exception as e:
                        print(f"Error with phrase_to_be_processed. Values - initial: {re.escape(initial)}, comparison_part: {comparison_part}, phrase_to_be_processed: {phrase_for_comparison}")
                        print(e)
                    
    return phrase_to_be_processed


def get_match_ratios(phrase1: list, phrase2=False) -> tuple[float, dict]:
    ''' Loops over the chunks of phrase sections of phrase1 and compares with the incrementally combined sections from phrase2 and gets the similarity ratios for each comparison. Returns the ratio for the best match (or matches) and the details of what was compared and the ratio for each comparison
    
        Key Arguments:
            phrase1 - list of phrase sections for comparison
            phrase2 - list of phrase sections for comparison
            
        Returns:
            Tuple with float ratio of best match between phrase chunks and dictionary with tuple containing the section of phrase2 being compared as "phrase2 start position: 
            phrase2 end position" and the similarity ration of the phrase1 phrase chunk to the section of phrase2 with the position of the phrase1 word chunk as the key
    '''

    match_matrix = {}
    anchor_ratio = 0
    
    for i in range(0, len(phrase1)):
        max_ratio = 0
        for j1 in range(0, len(phrase2)):
            for j2 in range (j1, len(phrase2)):
                combined_string = ''.join(phrase2[j1:j2+1])
                key = f"{str(j1)}:{str(j2+1)}"
                
                combined_string_no_punc = clean_string(combined_string)
                phrase2_no_punc = clean_string(phrase1[i])
                
                ratio = fuzz.ratio(phrase2_no_punc.lower(), combined_string_no_punc.lower())
                    
                if ratio > max_ratio:
                    match_matrix[i] = (key, ratio)
                    max_ratio = ratio
                    
                if ratio >= anchor_ratio:
                    anchor_ratio = ratio  
                    
    return (anchor_ratio, match_matrix)


def get_match_matrix(first_phrase: list, second_phrase: list, component_list: list) -> tuple[str, set]:
    ''' get the comparison matrix
    
        keyword arguments:
        phrase1 - the first list
        phrase2 - the second list
        word_ratio - dictionary of variation ratio
        
        return tuple with string containing combined values and warnings
    '''
    match_warnings = set()
    
    match_matrix_by_phrase1 = {}

    # by default, phrase1 should be shorter or the same length as phrase2
    if len(first_phrase) > len(second_phrase):
        phrase1 = second_phrase
        phrase2 = first_phrase
    else:
        phrase1 = first_phrase
        phrase2 = second_phrase     
    
    anchor_ratio, match_matrix_by_phrase1 = get_match_ratios(phrase1, phrase2)    
    
    best_anchor_points = []
    
    last_position_phrase2 = 0
    last_position_phrase1 = 0
    
    for phrase1_position, phrase2_details in match_matrix_by_phrase1.items():
        phrase2_position, best_ratio = phrase2_details
        phrase2_start = int(phrase2_position.split(":")[0])
        phrase2_end = int(phrase2_position.split(":")[1])  

        # make list of anchor points (points with highest match ratio)
        if best_ratio == anchor_ratio:
            if phrase1_position >= last_position_phrase1 and phrase2_end >= last_position_phrase2:
                last_position_phrase1 = phrase1_position
                last_position_phrase2 = phrase2_end                
                best_anchor_points.append((phrase1_position, phrase2_position))
    
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
                
                # if phrase1 is at start but phrase2 is before the first start point
                if phrase1_pointer == phrase1_start and phrase2_pointer < phrase2_start:
                    phrase2_token = ' '.join(phrase2[phrase2_pointer:phrase2_start])
                    
                    if len(anchored_list) > 0 and phrase2_pointer > 0:                       
                        # if the end of the last thing added to the anchored list is a comma, the end of the previous phrase2 section wasn't a comma and the end of the current section is a comma
                        try:
                            if str(anchored_list[-1])[-1] == "," and str(phrase2[phrase2_pointer - 1])[-1] != "," and phrase2_token[-1] == ",":
                                anchored_list[-1] = str(anchored_list[-1])[:-1]
                                phrase2_token = phrase2_token[:-1]
                                anchored_list.append(f"({phrase2_token}?)")
                            else:
                            
                                anchored_list.append(f"({phrase2_token}?)")
                        except Exception as e:
                            print(f"Exception thrown when trying to deal with anchored list: {e}")
                            print(f"{len(anchored_list)=}")
                            print(f"{anchored_list=}")
                            print(f"Last section of Anchored List: {anchored_list[-1]}")
                            print(f"Previous token: {phrase2[phrase2_pointer - 1]}")
                            print(f"New token: {phrase2_token}")
                           
                    phrase2_pointer = phrase2_start
                        
                # if pointer is before phrase1 start but phrase2 is at start point        
                elif phrase1_pointer < phrase1_start and phrase2_start == phrase2_pointer:
                    phrase1_token = phrase1[phrase1_pointer]
                    
                    if len(anchored_list) > 0 and phrase1_pointer > 0:
                        if str(anchored_list[-1])[-1] == "," and str(phrase1[phrase1_pointer - 1])[-1] != "," and phrase1_token[-1] == ",":
                            anchored_list[-1] = str(anchored_list[-1])[:-1]
                            phrase1_token = phrase1_token[:-1]
                            anchored_list.append(f"({phrase1_token}?)")
                        else:
                           anchored_list.append(f"({phrase1_token}?)")                    

                    phrase1_pointer += 1
                
                # if pointers for both phrase1 and phrase2 are at their respective start points        
                elif phrase2_start == phrase2_pointer and phrase1_start == phrase1_pointer:
                    phrase1_token = phrase1[phrase1_start] 
                    phrase2_token = ' '.join(phrase2[int(phrase2_start):int(phrase2_end)])                        
                    
                    if phrase2_token != phrase1_token:
                        token_ratio = token_distribution(component_list, [phrase1_token, phrase2_token])
                        #print("Combine two words called from match_matrix_by_phrase2 (pointers matched) with " + phrase1_token + " and " + phrase2_token)
                        
                        combined_token, combination_warnings = combine_two_words(phrase1_token, phrase2_token, token_ratio)
                        match_warnings.update(combination_warnings)
                    else:
                        combined_token = phrase1_token
                    
                    if combined_token.strip() != '':   
                        anchored_list.append(combined_token)

                    phrase2_pointer = phrase2_end
                    phrase1_pointer += 1
                    
                # if pointers for both phrase1 and phrase2 are before their respective start points     
                else:
                    phrase1_token = ' '.join(phrase1[phrase1_pointer:phrase1_start])
                    phrase2_token = ' '.join(phrase2[int(phrase2_pointer):int(phrase2_start)])
                    phrase1_pointer = phrase1_start
                    phrase2_pointer = phrase2_start
                    
                    phrase2_token = initials_replace(phrase2_token.strip(), phrase1_token.strip()) 
                    phrase1_token = initials_replace(phrase1_token.strip(), phrase2_token.strip())                                     
                    
                    token_ratio = token_distribution(component_list, [phrase2_token, phrase1_token])
                    combined_token, combination_warnings = combine_two_words(phrase1_token, phrase2_token, token_ratio)
                    match_warnings.update(combination_warnings)
                    
                    if combined_token.strip() != '':  
                        anchored_list.append(combined_token)
        
        if len(phrase2) > last_phrase2_anchored_point or len(phrase1) > phrase1_pointer:
            phrase1_end_token = ' '.join(phrase1[phrase1_pointer:])
            phrase2_end_token = ' '.join(phrase2[int(phrase2_end):])  
            
            phrase2_end_token = initials_replace(phrase2_end_token.strip(), phrase1_end_token.strip()) 
            phrase1_end_token = initials_replace(phrase1_end_token.strip(), phrase2_end_token.strip())  
            
            component_list = [phrase2_end_token, phrase1_end_token]                              
                    
            end_token_ratio = token_distribution(component_list, [phrase2_end_token, phrase1_end_token])
            
            if phrase2_pointer == len(phrase2):
                anchored_list.append(f"({phrase1_end_token}?)")
            elif phrase1_pointer == len(phrase1):
                anchored_list.append(f"({phrase2_end_token}?)")
            else:
                if " " in phrase1_end_token or " " in phrase2_end_token:
                    end_phrase_join, end_phrase_join_warnings = combine_two_phrases(set(component_list), component_list)
                    match_warnings.update(end_phrase_join_warnings)
                    if end_phrase_join.strip() != '':  
                        anchored_list.append(end_phrase_join)
                else:
                    combined_token, combination_warnings = combine_two_words(phrase1_end_token, phrase2_end_token, end_token_ratio)
                    if combined_token.strip() != '': 
                        anchored_list.append(combined_token)
                    match_warnings.update(combination_warnings)
        
    else:
        match_warnings.add(f"Could not find any strong anchor points. '{' '.join(phrase2)}' and '{' '.join(phrase1)}' appear to be distinct values.")
        anchored_list = phrase2 + ["/"] + phrase1 
        
    return (' '.join(anchored_list), match_warnings)
        

