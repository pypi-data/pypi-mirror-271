def get_inverse_char(num,string):
    
    inverse_num = len(string)-num
    

    return -(inverse_num+1)


from collections import defaultdict
import itertools
def longest_common_prefix(str1, str2):
    """Find the longest common prefix between two strings."""
    min_length = min(len(str1), len(str2))
    for i in range(min_length):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_length]

def longest_common_suffix(str1, str2):
    """Find the longest common suffix between two strings."""
    str1 = str1[::-1]
    str2 = str2[::-1]
    return longest_common_prefix(str1, str2)[::-1]

def get_inverse_char(index, str):
    """Return the character from the end based on the index from the start."""
    return len(str) - index - 1
def longest_common_prefix(str1, str2):
    """Find the longest common prefix between two strings."""
    min_length = min(len(str1), len(str2))
    for i in range(min_length):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_length]

def longest_common_suffix(str1, str2):
    """Find the longest common suffix by reversing strings and using longest_common_prefix."""
    str1 = str1[::-1]
    str2 = str2[::-1]
    return longest_common_prefix(str1, str2)[::-1]

def get_inverse_char(index, str):
    """Return the character from the end based on the index from the start."""
    return len(str) - index - 1

def check_inverse_char_presence(header, comp_header):
    """Check the presence of each inverse character from 'header' in 'comp_header'."""
    inverse_presence = []
    for i in range(len(header)):
        inverse_char = header[get_inverse_char(i, header)]
        if inverse_char in comp_header:
            inverse_presence.append((inverse_char, True))
        else:
            inverse_presence.append((inverse_char, False))
    return inverse_presence
def find_unique_matches(list1, list2):
    """
    Finds unique substring matches between two lists of strings.
    
    Parameters:
        list1 (list): The first list of strings.
        list2 (list): The second list of strings.
        
    Returns:
        dict: A dictionary of unique matches where each key-value pair is a unique relationship.
    """
    matches = {}

    # Check each string in the first list against each string in the second list
    for str1 in list1:
        for str2 in list2:
            if str1 in str2 or str2 in str1:
                # Check if either string already has a match registered
                if str1 not in matches and str2 not in matches.values():
                    matches[str1] = str2
                elif str1 in matches:
                    # If already matched but found another, remove and note as non-unique
                    if matches[str1] != str2:
                        del matches[str1]
                        break
                elif str2 in matches.values():
                    # Find the key for the current value str2 and remove it for being non-unique
                    key_to_remove = [key for key, value in matches.items() if value == str2][0]
                    del matches[key_to_remove]

    return matches


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

comp_headers = """Source.Name	INPUT: Extra 3	Date Pulled	Code	INPUT: Extra 1	INPUT: First Name	INPUT: Middle Name	INPUT: Last Name	INPUT: Address 1	INPUT: Address 2	INPUT: City	INPUT: State	ZIP	INPUT: Extra 4	INPUT: Extra 5	INPUT: Extra 6	PH: Phone1	EMAIL: Email1""".split('\t')
df = "/home/gamook/Documents/pythonScripts/test_grounds/all_excels/originals/ALL Time Data for Solar.xlsx"
df = get_df(df)
headers = df.columns.tolist()
headlower = [str(head).lower() for head in headers]
comp_lowers = [str(comp).lower() for comp in comp_headers]
# Lowercase versions of headers

# Find and print the best unique matches
best_matches = {}
matches = main(comp_lowers, headlower)
for key,value in matches.items():
    if key in comp_lowers:
        comp_lowers.remove(key)
    if value in comp_lowers:
        comp_lowers.remove(value)
        
    if key in headlower:
        headlower.remove(key)
    if value in headlower:
        headlower.remove(value)
    best_matches[key]=value
input(best_matches)
matches = find_unique_matches(comp_lowers, headlower)

input(matches)
for key,value in matches.items():
    if key in comp_lowers:
        comp_lowers.remove(key)
    if key in headlower:
        headlower.remove(key)
    if value in comp_lowers:
        comp_lowers.remove(value)
    if value in headlower:
        headlower.remove(value)
    best_matches[key]=value

input(comp_lowers)
results = []
highest = [None,None]
for i,comp_lower in enumerate(comp_lowers):
    if i!= 0:
        prefix = longest_common_prefix(comp_lowers[i-1], comp_lowers[i])
        common = [obj for obj in comp_lowers if obj.startswith(prefix)]
        if highest[0] == None:
            highest=[prefix,common]
        else:
            if len(prefix)>len(highest[0]):
                highest=[prefix,common]
comp_lowers = [obj[len(prefix):] for obj in highest[1]]+[obj for obj in comp_lowers if obj not in highest[1]]
comp_lowers_pre = highest[1]+[obj for obj in comp_lowers if obj not in highest[1]]
highest = [None,None]
for i,headlow in enumerate(headlower):
    if i!= 0:
        prefix = longest_common_prefix(headlower[i-1], headlower[i])
        common = [obj for obj in headlower if obj.startswith(prefix)]
        if highest[0] == None:
            highest=[prefix,common]
        else:
            if len(prefix)>len(highest[0]):
                highest=[prefix,common]
headlower = [obj[len(prefix):] for obj in highest[1]]+[obj for obj in headlower if obj not in highest[1]]

headlowers_pre = highest[1]+[obj for obj in headlower if obj not in highest[1]]
matches = main(comp_lowers, headlower)
for key,value in matches.items():
    if key in comp_lowers_pre:
        comp_lowers_pre.remove(key)
    if key in headlowers_pre:
        headlowers_pre.remove(key)
    if value in comp_lowers_pre:
        comp_lowers_pre.remove(value)
    if value in headlowers_pre:
        headlowers_pre.remove(value)
    best_matches[key]=value
input(matches)
results = []
# Comparing each string in the computed headers list against each string in the original headers list
input(get_closest_headers(df,comp_lowers))
for comp_header in comp_lowers:
    for header in headlower:
        prefix = longest_common_prefix(comp_header, header)
        suffix = longest_common_suffix(comp_header, header)

        # Calculate non-matching middle part indices
        middle_start = len(prefix)
        middle_end = len(comp_header) - len(suffix)
        middle = comp_header[middle_start:middle_end] if middle_end > middle_start else ''

        # Check for inverse character presence
        inverse_presence = check_inverse_char_presence(header, comp_header)

        results.append({
            'header': header,
            'comp_header': comp_header,
            'common_prefix': calculate_match_score(prefix, header),
            'common_suffix': calculate_match_score(suffix, header),
            'middle': calculate_match_score(middle, header),
            'inverse_presence':calculate_match_score([pres[0] for pres in inverse_presence if pres[1]], inverse_presence),
            'unique_match':find_unique_matches([header], comp_lowers)
        })

input(results)
