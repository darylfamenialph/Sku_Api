import re


def generate_sku(input_string, iteration):
    # Setting Iterations
    if iteration == 0:
        normal_initial = 3
        lower_upper_case_initial = 2
    elif iteration == 1:
        normal_initial = 4
        lower_upper_case_initial = 2
    elif iteration == 2:
        normal_initial = 5
        lower_upper_case_initial = 2
    elif iteration == 3:
        normal_initial = 6
        lower_upper_case_initial = 2
    elif iteration == 4:
        normal_initial = 7
        lower_upper_case_initial = 2
    else:
        normal_initial = 3
        lower_upper_case_initial = 2

    # Setting up global variables
    string_input = input_string
    original = input_string
    un_necessaries = ("(GSM)", "(Global)", "(CDMA)", "(China")
    special_models = ("iPad",)

    # Removing Un-necessary words
    for un_necessary in un_necessaries:
        string_input = string_input.replace(un_necessary, '')

    # Setting up Regex Variables
    special_chars = re.compile(r"[^a-zA-Z0-9\s]")
    lower_case_first_char = re.compile(r"^[a-z][a-z\d._]*s?")
    letters_with_num = re.compile(r"(\d+)(?!.*\d)")
    unknown_pattern = re.compile(r"^[a-z][a-z\d._]*$")

    matches = special_chars.finditer(string_input)
    for match in matches:
        string_input = string_input.replace(match.group(), '')

    # Split input strings separated with space
    split_strings_input = string_input.split(' ')
    split_count = len(split_strings_input)

    result = ""
    if split_count > 1:
        for split_string in split_strings_input:
            lower_case_first_char_match = lower_case_first_char.finditer(split_string)
            lower_case_first_char_match = tuple(lower_case_first_char_match)
            if len(lower_case_first_char_match) > 0:
                if split_string in special_models:
                    result = result + split_string[:normal_initial]
                else:
                    result = result + split_string[:lower_upper_case_initial]
            else:
                if len(split_string) <= 3:
                    result = result + split_string
                else:
                    result = result + split_string[:1]
    else:
        string_match = letters_with_num.finditer(string_input)
        string_match = tuple(string_match)
        if len(string_match) > 0:
            string_input_trimmed = string_input.replace(string_match, '')
            if len(string_input_trimmed) <= 2:
                result = result + string_input
            else:
                first_2_char = string_input[:2]
                for result_string in string_match:
                    string_input = string_input.replace(result_string.group())
                result = first_2_char + string_input
        else:
            if len(string_input) > 2:
                lower_case_first_char_match = lower_case_first_char.finditer(string_input)
                lower_case_first_char_match = tuple(lower_case_first_char_match)
                if len(lower_case_first_char_match) > 0:
                    if string_input in special_models:
                        result = result + string_input[:normal_initial]
                    else:
                        result = result + string_input[:lower_upper_case_initial]
                else:
                    if normal_initial < len(string_input):
                        result = result + string_input[:normal_initial]
                    else:
                        result = result + string_input
            else:
                result = result + string_input

    return f"{result.upper()}"


if __name__ == '__main__':
    result = generate_sku("iPhone Xs Max Pro", 0)
    print(result)

