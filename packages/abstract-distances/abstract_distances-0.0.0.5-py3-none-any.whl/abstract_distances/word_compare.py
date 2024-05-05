from collections import defaultdict
import itertools,re
from .excel_module import get_df,pd
def compare_strings(s1, s2):
    """
    Compares two strings to check if they are the same length and identical in all characters
    except possibly within numeric characters. Returns the differing numbers if found.

    Parameters:
        s1 (str): The first string to compare.
        s2 (str): The second string to compare.

    Returns:
        tuple: (bool, list) where bool indicates if the strings match under the given conditions,
               and list contains the pairs of differing numbers if any.
    """
    
    # Check if the strings are the same length
    if len(s1) != len(s2):
        return (False, [])

    # Find all numbers in both strings
    numbers_s1 = re.findall(r'\d+', s1)
    numbers_s2 = re.findall(r'\d+', s2)

    # Replace digits in both strings with '0' to compare non-numeric parts
    transformed_s1 = re.sub(r'\d', '0', s1)
    transformed_s2 = re.sub(r'\d', '0', s2)

    if transformed_s1 != transformed_s2:
        return (False, [])

    # Comparing the numbers in the same order they appear
    differing_numbers = []
    for num1, num2 in zip(numbers_s1, numbers_s2):
        if num1 != num2:
            differing_numbers.append((num1, num2))

    # If the non-numeric parts are identical and the numeric parts have differences
    if differing_numbers:
        return (True, differing_numbers)
    else:
        # If there are no numeric differences
        return (True, [])

def get_most_original_from_ls(string, values_list,string_list):
    strings = [string,'']
    for string_2 in values_list:
        strings[1] = string_2
        bool_comp,string_comp = compare_strings(string, string_2)
        
        if bool_comp and string_comp and bool_comp not in string_list:
            lowest = None
            for i,each in enumerate(string_comp[0]):
                each=int(each)
                if lowest == None or lowest[1] > each:
                    lowest=[i,each]
            return strings[lowest[0]]
    return string
def calculate_match_score(str1, str2):
    """
    Calculates a match score based on the length of the longest common substring
    relative to the string lengths.
    """
    if str1 and str2:#[float(0),0,None,'nan','NaN']
        if str1 in str2:
            return len(str1) / len(str2)
        elif str2 in str1:
            return len(str2) / len(str1)
    return 0

def find_best_unique_matches(list1, list2):
    """
    Identifies the best matches based on substring content and uniqueness.
    
    Parameters:
        list1 (list): The first list of strings.
        list2 (list): The second list of strings.
        
    Returns:
        dict: A dictionary with best unique matches.
    """
    potential_matches = {}
    for str1 in list1:
        for str2 in list2:
            score = calculate_match_score(str1, str2)
            if score > potential_matches.get((str1, str2), 0):
                potential_matches[(str1, str2)] = score

    # Filter to ensure uniqueness and best scores
    best_matches = {}
    for (str1, str2), score in potential_matches.items():
        if str1 not in best_matches and all(str2 != match for match in best_matches.values()):
            best_matches[str1] = str2
        elif str1 in best_matches:
            current_match = best_matches[str1]
            if potential_matches[(str1, current_match)] < score:
                best_matches[str1] = str2

    return best_matches
def find_commons_dna(list1, list2,new_matches={}):
    # Step 1: Remove common substrings within each list to simplify strings
    common_subs_list1 = find_common_substrings(list1)
    common_subs_list2 = find_common_substrings(list2)
    cleaned_list1 = remove_common_substrings(list1, common_subs_list1)
    cleaned_list2 = remove_common_substrings(list2, common_subs_list2)
    # Step 2: Calculate best matches based on cleaned lists
    best_matches = find_best_unique_matches(cleaned_list1, cleaned_list2)

    for key,value in best_matches.items():
        if key or value:
            i =0
            for clean_1 in cleaned_list1:       
                if clean_1 == key:
                    key = list1[i]
                    break
                i +=1 
            i =0
            for clean_2 in cleaned_list2:
                if clean_2 == value:
                    value = list2[i]
                    break
                i +=1   
            new_matches[key]=value
    
    for key,value in new_matches.items():
        if key in list1:
            list1.remove(key)
        if value in list1:
            list1.remove(value)
            
        if key in list2:
            list2.remove(key)
        if value in list2:
            list2.remove(value)
        best_matches[key]=value
    return new_matches,list1,list2
def find_common_substrings(strings, min_length=1):
    """
    Finds common substrings among a list of strings.
    
    Parameters:
        strings (list): List of input strings.
        min_length (int): Minimum length of substring to consider.
        
    Returns:
        set: A set containing all substrings found in more than one string.
    """
    common_substrings = defaultdict(int)
    substring_set = set()

    # Generate all possible substrings for each string
    for string in strings:
        for start in range(len(string)):
            for end in range(start + min_length, len(string) + 1):
                substring = string[start:end]
                common_substrings[substring] += 1
                if common_substrings[substring] > 1:
                    substring_set.add(substring)

    return substring_set

def remove_common_substrings(strings, common_subs):
    """
    Removes common substrings from a list of strings.
    
    Parameters:
        strings (list): List of strings to process.
        common_subs (set): Set of substrings to remove.
        
    Returns:
        list: Updated list of strings with common substrings removed.
    """
    updated_strings = []
    for string in strings:
        for sub in common_subs:
            string = string.replace(sub, '')
        updated_strings.append(string)
    return updated_strings

def get_closest_headers(df,*args,**kwargs):
    df=get_df(df)
    convert_list = ["address","city","state","zip","external","phone","distance","fico","middle name","last name","full name","email"]
    for arg in args:
        if isinstance(arg,list):
            convert_list+=arg
        elif isinstance(arg,pd.DataFrame):
            headers = arg.columns.tolist()
            convert_list+=headers
        else:
            convert_list.append(arg)
    convert_list=list(set(convert_list))
    headers = df.columns.tolist()
    closest_js={str(key):safe_get([item for item in headers if (key.lower() in item.lower() or item.lower() == key.lower())],0) or "" for key in convert_list}
    headers = [head for head in headers if head not in list(closest_js.values())]
    convert_list = [head for head in convert_list if head not in list(closest_js.keys())]
    for key,value in find_best_unique_matches(convert_list, headers):
        closest_js[key]=value
    headers = [head for head in headers if head not in list(closest_js.values())]
    convert_list = [head for head in convert_list if head not in list(closest_js.keys())]
    for key,values in closest_js.items():
        for comp_key in headers:
            if comp_key.lower() == key:
                closest_js[key]=comp_key
                break
        if closest_js[key] == "":
            matches = {}
            for comp_key in headers:
                if comp_key not in list(closest_js.values()):
                    for char in key:
                        if char in comp_key.lower():
                            if comp_key not in matches:
                                matches[comp_key]=[]
                            if len(matches[comp_key])==0:
                                matches[comp_key].append('')
                            if matches[comp_key][-1]+char in comp_key.lower():
                                matches[comp_key][-1]+=char
                            else:
                                matches[comp_key].append(char)
            for header,values in matches.items():
                len_header = len(header)
                highest=[0,'']
                for val in values:
                    if len(val)>highest[0]:
                        highest=[len(val),val]
                matches[header]={'perc':highest[0]/len_header,'value':highest[1]}
            highest=[0,'']
            for header,val in matches.items():
                if val['perc']>highest[0]:
                    highest=[val['perc'],header]
            closest_js[key] = get_most_original_from_ls(highest[-1],headers, closest_js.values())
    return closest_js

