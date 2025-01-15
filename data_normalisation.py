# Compare and normalise data from multiple columns
#   
#   Select columns to compare
#   Put values into Set to see how many unique values there are
#   Tokenize each words
#   Check number of tokens
#   If there are more then one then check distribution
#   
#

#####################
#   To Do:
#
#   Deal with spaces in the wrong places e.g. Hill Stone vs Hillstone
#   Deal with addresses

from rapidfuzz import fuzz
import difflib, re, itertools




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
        component_list_caseless = [component.lower() for component in component_list if (component.strip() != "" and component.strip() != "*")]   
        alt_component_set = set([("".join(component.split())).lower() for component in component_list if (component.strip() != "" and component.strip() != "*")] )


        # does the default set have the same number of values as the set with all the spaces and cases removed
        if len(component_set) != len(alt_component_set):
            component_set_caseless = set([component.lower() for component in component_list if (component.strip() != "" and component.strip() != "*")])  
                     
            # does the default set and the caseless set not have the same length while the caseless and the space+caseless have the same length
            if len(component_set) != len(component_set_caseless) and len(alt_component_set) == len(component_set_caseless):
                #print("Case Issue")
                
                #Assumption: Case mismatch - convert to title case.
                component_set = {item.title() for item in component_set}
                
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
                            processed_list.append(grouped_list[0].title())                       
                    
                    #string1 = list(component_set_caseless)[0]
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
                    matched_value = re.sub(r'(\?)?\) \(', ' ', matched_value)
                    component_set = set([matched_value])
                    warnings[key].update(matched_warnings)
                    
                    #print(component_set)
       
        #distribution = split_distribution(component_list)
        #distribution = split_part_distribution(component_list)

        if len(component_set) < 2:  # One version
            basic_join = "".join([component for component in component_set])
            if debug:
                print("Basic join - " + key + ": " + basic_join)
            combined_values[key] = basic_join
        elif len(component_set) == 2:   # Two variations
            two_phrase_join, two_phrase_join_warnings = combine_two_phrases(component_set, component_list, debug)
            two_phrase_join = re.sub(r'(\?)?\) \(', ' ', two_phrase_join)
            #print("Two phase warnings:" + str(two_phrase_join_warnings))
            warnings[key].update(two_phrase_join_warnings)
            if debug:
                print("Two part join - " + str(key) + ": " + two_phrase_join)
                print("Component set: " + str(component_set))
                print("Component list: " + str(component_list))
            combined_values[key] = two_phrase_join
        else:   # More than two variations
            
            #print(component_set)
            warnings[key].add("Warning: Attempting to combine multiple (>2) variations.")
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
                    print(key + ": Option E")
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
                warnings[key].update(part_sub_set_warnings)
                part_combined_phrases = re.sub(r'\(+', '(', part_combined_phrases)
                part_combined_phrases = re.sub(r'(\?\))+', '?)', part_combined_phrases)
                
                for i in range (0, len(best_similar_list)):
                    modified_best_similar_list.append(part_combined_phrases)
                
                similar = similar.difference(best_similar)
                similar.add(part_combined_phrases)
 
            combined_phrases = re.sub(r'(\?)?\) \(', ' ', "".join(list(similar)))
            
            if len(distinct) > 0:
                combined_values[key] = combined_phrases + "/(" + "?/ ".join(distinct) + "?)" 
            else:
                combined_values[key] = combined_phrases
    
    print(combined_values)
    #print(warnings)
                
    return (combined_values, warnings)
                   
                
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


def combine_two_phrases(component_set, component_list, debug=False):
    #print(key + ": " + ", ".join([component for component in component_set]))
    #print(key + ": ")

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
    ''' Combine two words
    
        Keyword arguments:
        component1 - single word string
        component2 - single word string
        word_ratio - dictionary of variation ratio
        debug - boolean, False by default, if True print out debug
        
        returns string with combined values
    '''
    
    ratio = fuzz.ratio(component1, component2)
    ratio_caseless = fuzz.ratio(component1.lower(), component2.lower())
    ratio_caseless_no_punc = fuzz.ratio(re.sub(r'[^\w\s]', '', component1.lower()), re.sub(r'[^\w\s]', '', component2.lower()))
       
    if debug:
        print("component1: " + component1)
        print("component2: " + component2)
        print("distribution: " + str(word_ratio))
        print("ratio: " + str(ratio))
        print("ratio (caseless): " + str(ratio_caseless))
        
    if ratio_caseless_no_punc == 100:
        if len(component1) > len(component2):
            return component1.title() 
        else:
            return component2.title()
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
                if ratio_caseless > ratio:
                    diff = difflib.Differ().compare(component1.lower(), component2.lower())
                else:
                    diff = difflib.Differ().compare(component1, component2)   
                
                generated_string_list = [s.strip() if s[0] == ' ' else '(' + s[-1] + '?)' for s in diff]
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
    generated_string = ''.join(generated_string_list)
    
    if ratio_caseless > ratio:
        generated_string = generated_string.title()
        
    if debug:
        print(generated_string_list)
        print("Generated string: " + generated_string)
        
    return generated_string


def align_two_phrases(string1, string2, component_list, debug=False):
    ''' Check if two strings align and return a combined version

        keyword arguments:
        string 1 - the first phrase
        string 2 - the second phrase
        component_list - list of components
        debug - boolean, False by default, if True print out debug
        
        returns tuple with string with combined values and warnings
    '''
    if debug:
        print("align_two_phrases called with '" + str(string1) + "' & '" + str(string2) + "'" )
    
    #diff = difflib.Differ().compare(string1, string2)
    #print("\n".join(diff))
    
    #components1 = string1.split(" ")
    #components2 = string2.split(" ")
    
    combined = ""
    
    warnings = {"Note: Combining multi-length variations."}
    
    if len(string1) > len(string2):
        longest = string1
        shortest = string2
    else:
        longest = string2
        shortest = string1       

    if debug:
        print("longest: " + str(longest))
        print("shortest: " + str(shortest))
   
    aligned_phrase, phrase_warnings = get_match_matrix(longest, shortest, component_list, debug)
    
    warnings.update(phrase_warnings)
    
    if debug:
        print(aligned_phrase)
        
    return (aligned_phrase, warnings)
    

def initials_replace(phrase_to_be_processed, phrase_for_comparison, debug=False):
    
    if True in [True for part in phrase_to_be_processed.split(' ') if len(re.sub(r'[^\w\s]', '', part)) < 2]:
        
        initials = [part for part in phrase_to_be_processed.split(' ') if len(re.sub(r'[^\w\s]', '', part)) < 2]
        if debug:        
            print("\nInitials: " + str(initials))
        
        for initial in initials:
            initial_no_punc = re.sub(r'[^\w\s]', '', initial)
            for comparison_part in phrase_for_comparison.split(' '):
                if debug: 
                    print("Comparison part: " + comparison_part)
                if initial_no_punc == comparison_part[0]:
                    phrase_to_be_processed = re.sub(r'^'+initial+r'(\s|$)', comparison_part, phrase_to_be_processed)
                    if debug: 
                        print("Processed phrase: " + phrase_to_be_processed + "\n")   
                    
    return phrase_to_be_processed

def get_match_matrix(longest, shortest, component_list, debug=False):
    ''' get the comparison matrix
    
        keyword arguments:
        longest - the longest list 
        shortest - the shortest list
        word_ratio - dictionary of variation ratio
        debug - boolean, False by default, if True print out debug
        
        return tuple with string containing combined values and warnings
    '''
    #debug = True
    match_warnings = set()
    
    match_matrix = {}
    #print(longest)
    #print(shortest)
    
    #for i in range(0, len(longest)):
    #    match_matrix[i] = {j: fuzz.ratio(longest[i], shortest[j]) for j in range(0, len(shortest))}
    
    #print("Form each in longest:")
    #print(match_matrix)
    
    anchor_ratio = 0
        
    for i in range(0, len(shortest)):
        max_ratio = 0
        for j1 in range(0, len(longest)):
            for j2 in range (j1, len(longest)):
                combined_string = ''.join(longest[j1:j2+1])
                key = str(j1) + ":" + str(j2+1)
                
                combined_string_no_punc = re.sub(r'[^\w\s]', '', combined_string)
                shortest_no_punc = re.sub(r'[^\w\s]', '', shortest[i])
                
                #if debug:
                #    print(combined_string_no_punc)
                #    print(shortest_no_punc)
                
                ratio = fuzz.ratio(shortest_no_punc.lower(), combined_string_no_punc.lower())
                
                if debug: 
                    combo = "A" + str(i) + "-B" + ": " + str(j1) + "-" + str(j2) + " (" + shortest[i].lower() + "-" + combined_string.lower() +  ") = " + str(ratio)
                    print(combo)
                    
                if ratio > max_ratio:
                    match_matrix[i] = (key, ratio)
                    max_ratio = ratio
                    
                if ratio >= anchor_ratio:
                    anchor_ratio = ratio                

    if debug:
        print("For each in shortest:")        
        print(match_matrix)
    
    best_anchor_points = []
    
    last_position_shortest = 0
    last_position_longest = 0
    
    for short_position, long_details in match_matrix.items():
        long_position, best_ratio = long_details
        long_start = int(long_position.split(":")[0])
        long_end = int(long_position.split(":")[1])   
        
        # make list of anchor points (points with highest match ratio)
        if best_ratio == anchor_ratio:
            if short_position >= last_position_shortest and long_end >= last_position_longest:
                last_position_shortest = short_position
                last_position_longest = long_end
                
                best_anchor_points.append((short_position, long_position))
                
    if debug:
        print(str(anchor_ratio))
        print(best_anchor_points)
        print("longest: " + str(longest) + ",  length: " + str(len("".join(longest))))
    
    if ratio_check(len("".join(longest)), anchor_ratio):
        anchored_list = []
        long_pointer = 0
        short_pointer = 0
        last_longest_anchored_point = 0
        
        for anchor_points in best_anchor_points:
            short_start, long_range = anchor_points
            long_start = int(long_range.split(":")[0])
            long_end = int(long_range.split(":")[1])
            shortest_token = ""
            longest_token = ""
            last_longest_anchored_point = long_end
            
            # while short pointer is pointing at or before the short start and the long pointer has not reached the end of the long values
            while short_pointer <= short_start and long_pointer <= long_end:
                if debug:
                    print("Before - Short pointer: " + str(short_pointer) + ", short start: " + str(short_start)) 
                    print("Before - Long pointer: " + str(long_pointer) + ", long start: " + str(long_start)) 
                
                # if short is at start but long is before the first start point
                if short_pointer == short_start and long_pointer < long_start:
                    longest_token = ' '.join(longest[long_pointer:long_start])
                    anchored_list.append("(" + longest_token + "?)")
                    long_pointer = long_start
                    
                    if debug:
                        print("Added 'long' string to bring into alignment")
                        print("Adding (longest): " + longest_token)
                        print("Long pointer: " + str(long_pointer))
                        
                # if pointer is before short start but long is at start point        
                elif short_pointer < short_start and long_start == long_pointer:
                    shortest_token = shortest[short_pointer]
                    short_pointer += 1
                    anchored_list.append("(" + shortest_token + "?)")
                    
                    if debug:
                        print("Added 'short' string to bring into alignment")
                        print("Adding (shortest): " + shortest_token)
                        print("Short pointer: " + str(short_pointer))
                
                # if pointers for both long and short are at their respective start points        
                elif short_start == short_pointer and long_start == long_pointer:
                    shortest_token = shortest[short_start] 
                    longest_token = ' '.join(longest[int(long_start):int(long_end)])                        
                    
                    if shortest_token != longest_token:
                        token_ratio = token_distribution(component_list, [shortest_token, longest_token], debug)
                        combined_token = combine_two_words(longest_token, shortest_token, token_ratio, debug)
                        
                        if debug:
                            print("Added combined section")
                            print("Shortest token: " + shortest_token)
                            print("Longest token: " + longest_token)
                            print("Token ratio: " + str(token_ratio))
                            print("Adding (combined match): " + combined_token)
                    else:
                        combined_token = shortest_token
                        
                    anchored_list.append(combined_token)
                    long_pointer = long_end
                    short_pointer += 1
                    
                # if pointers for both long and short are before their respective start points     
                else:
                    shortest_token = ' '.join(shortest[short_pointer:short_start])
                    longest_token = ' '.join(longest[int(long_pointer):int(long_start)])
                    long_pointer = long_start
                    short_pointer = short_start
                    
                    shortest_token = initials_replace(shortest_token, longest_token, debug) 
                    longest_token = initials_replace(longest_token, shortest_token, debug)                                     
                    
                    token_ratio = token_distribution(component_list, [shortest_token, longest_token], debug)
                    combined_token = combine_two_words(longest_token, shortest_token, token_ratio, debug)
                    
                    anchored_list.append(combined_token)
                    
                    if debug:
                        print("Adding combined starting string")
                        print("Shortest token: " + shortest_token)
                        print("Longest token: " + longest_token)
                        print("Token ratio: " + str(token_ratio))
                        print("Adding (combined gap): " + combined_token)
                                    
                if debug:
                    print("After - Short: " + shortest_token + ", pointer: " + str(short_pointer))
                    print("After - Long: " + longest_token + ", pointer: " + str(long_pointer))                    
        
        if len(longest) > last_longest_anchored_point or len(shortest) > short_pointer:
            shortest_end_token = ' '.join(shortest[short_pointer:])
            longest_end_token = ' '.join(longest[int(long_end):])  
            
            shortest_end_token = initials_replace(shortest_end_token, longest_end_token, debug) 
            longest_end_token = initials_replace(longest_end_token, shortest_end_token, debug)  
            
            component_list = [shortest_end_token, longest_end_token]                              
                    
            #end_token_ratio = token_distribution(component_list, [shortest_end_token, longest_end_token], debug)
            
            if debug:
                print("Adding end section")
                print("Short pointer: " + str(short_pointer) + ", short end: " + str(len(shortest))) 
                print("Long pointer: " + str(long_pointer) + ", long end: " + str(len(longest))) 
                print("component list: " + str(component_list))
            
            if short_pointer == len(shortest):
                anchored_list.append("(" + longest_end_token + "?)")
            elif longest_end_token == len(longest):
                anchored_list.append("(" + shortest_end_token + "?)")
            else:
                #combined_token = combine_two_words(longest_end_token, shortest_end_token, end_token_ratio, debug)
                end_phrase_join, end_phrase_join_warnings = combine_two_phrases(set(component_list), component_list, debug)
                match_warnings.update(end_phrase_join_warnings)
                anchored_list.append(end_phrase_join)
        
        if debug:
            print(anchored_list)        
        
    else:
        match_warnings.add("Could not find any strong anchor points. '" + " ".join(shortest) + "' and '" + " ".join(longest) + "' appear to be distinct values.")
        anchored_list = shortest + ["/"] + longest 
        
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

def get_similarity_range(values, get_min = True, get_max = True):
    
    flattened_values = []
    for value in values:
        if isinstance(value, str) and (value.strip() and value.strip() != "*"):
            flattened_values.append(value)
        elif isinstance(value, list):
            value = [x for x in value if x.strip() and x.strip() != "*"]
            flattened_values += value
    
    values_set = set(flattened_values)
    
    if len(values_set) == 1:
        min = 100
        max = 100
    else:
        max = 0
        min = 100
        for i, value1 in enumerate(list(values_set)):
            for j, value2 in enumerate(list(values_set)):
                if i != j:
                    ratio = fuzz.ratio(value1, value2)
                    if ratio > max:
                        max = ratio
                    if ratio < min:
                        min = ratio
                        
    if get_min and get_max:
        return (min, max)
    elif get_min:
        return min
    else:
        return max
        
    
        


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
         "17": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"]                   
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

#component_compare(names1)
component_compare(names2)
#component_compare(address)
#component_compare(farm_name)
#component_compare(test)
#component_compare(test2)
#component_compare(test3)