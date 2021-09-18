import re

import ipdb
def f(): pass
#ipdb.set_trace = f

units = {
        "zero" : "0'",
        "a" : "1", # "a million"
        "one" : "1",
        "two" : "2",
        "three" : "3",
        "four" : "4",
        "five" : "5",
        "six" : "6",
        "seven" : "7",
        "eight" : "8",
        "nine" : "9",
}

teens = {
        "ten" : "10",
        "eleven" : "11",
        "twelve" : "12",
        "thirteen" : "13",
        "fourteen" : "14",
        "fifteen" : "15",
        "sixteen" : "16",
        "seventeen" : "17",
        "eighteen" : "18",
        "nineteen" : "19",
    }

tens = {
    "twenty" : '2',
    "thirty" : '3',
    "forty" : '4',
    "fifty" : '5',
    "sixty" : '6',
    "seventy" : '7',
    "eighty" : '8',
    "ninety" : '9',
}

scales = {
    "thousand" : 3, # 10^3
    "million" : 6, # 10^6
    "billion" : 9, # 10^9
    # "trillion", # 10^12
    # "quadrillion", # 10^15
    # "quintillion", # 10^18
    # "sextillion", # 10^21
    # "septillion", # 10^24
    # "octillion", # 10^27
    # "nonillion", # 10^30
    # "decillion", # 10^33
    # "undecillion", # 10^36
    # "dodecillion", # 10^39
    # "tredecillion", # 10^42
    # "quattuordecillion", # 10^45
    # "quindecillion", # 10^48
    # "sexdecillion", # 10^51
    # "septendecillion", # 10^54
    # "octodecillion", # 10^57
    # "novemdecillion", # 10^60
    # "vigintillion", # 10^63
}

def period_rep(tokens, period_start_loc, period_end_loc):
    # parse a "period" of the number corresponding to 3 digits
    str_ = ''

    first_digit = '0'
    if 'hundred' in tokens[period_start_loc:period_end_loc]:
        # The token before "hundred" must be the number of hundreds
        hundred_idx = tokens.index('hundred')
        first_digit = units[tokens[hundred_idx - 1]]  # Should raise KeyError if malformed input
        period_start_loc += 2
    str_ += first_digit

    second_digit = '0'
    for t in tens:
        if t in tokens[period_start_loc:period_end_loc]:
            second_digit = tens[t]
            period_start_loc += 1
    str_ += second_digit

    third_digit = '0'
    for u in units:
        if u in tokens[period_start_loc:period_end_loc]:
            third_digit = units[u]
            period_start_loc += 1 # Though this is not used currently, leave it here for extensions like "ninety eight point six degrees"
    str_ += third_digit

    # Handle the case of 11 - 19
    for te in teens:
        if te in tokens[period_start_loc:period_end_loc]:
            str_ = str_[0] + teens[te] # Can't do in-place because of 'str' object does not support item assignment

    return str_

def is_token_numeric(token, commas=False):
    if not commas:
        return token != ',' and (token in units or token in tens or token in scales or token == 'hundred' or token in teens)
    return token in units or token in tens or token in scales or token == 'hundred' or token in teens

def find_continugous_number_words(tokens):
    number_words = []
    start_idcs = []
    end_idcs = []

    t_idx = 0
    new_word = True
    while t_idx < len(tokens):
        if is_token_numeric(tokens[t_idx]): # What about commas and hyphens and "and"?
            if new_word:
                start_idx = t_idx
                start_idcs.append(t_idx)
                new_word = False
        else:
            if not new_word:
                number_words.append(tokens[start_idx:t_idx])
                end_idcs.append(t_idx)
            new_word = True
        t_idx += 1

    return number_words, list(zip(start_idcs, end_idcs))

def parse_number_word(number_tokens):
    # If there's a hyphen, split
    word_rep = ' '.join(number_tokens)
    word_rep = word_rep.replace('-', ' ')
    word_rep = word_rep.replace(' and ', ' ')
    tokens = re.split('( |,)', word_rep)
    tokens = list(filter(lambda x: x != ' ' and x != '', tokens))

    num_string = ''

    last_found_period = None
    for period in list(scales)[::-1]:  # Do them backwards to look for biggest scale first. As of Python 3.6, for the CPython implementation of Python, dictionaries maintain insertion order by default.
        if period in tokens:
            if last_found_period is not None:
                num_string += '0' * 3 * (list(scales).index(last_found_period) - list(scales).index(period) - 1)

            last_found_period = period
            period_end_loc = tokens.index(period)

            # walk backwards to find comma or non-number word
            period_start_loc = period_end_loc - 1
            token = tokens[period_start_loc]
            while is_token_numeric(token) and token not in scales and period_start_loc != 0: # Don't wrap around the string, walk back towards the last seen "scale" number like million, billion, etc.
                period_start_loc -= 1
                token = tokens[period_start_loc]

            num_string += period_rep(tokens, period_start_loc, period_end_loc)

    if last_found_period is not None and last_found_period != 'thousand':
        num_string += '0' * 3 * (list(scales).index(last_found_period))

    # Trim leading 0s
    num_string = num_string.lstrip('0')

    # If the last word is not a scale, then we have a number less than one thousand
    if last_found_period is None:
        num_string += period_rep(tokens, 0, len(tokens))
    elif tokens.index(last_found_period) != len(scales):
        num_string += period_rep(tokens, tokens.index(last_found_period)+1, len(tokens))
    else:
        num_string += '0' * scales[last_found_period] # Add right-zeros in the case we had a number like "one million"

    return num_string


def text2int(sentence):
    '''
    Loosely adapted from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
    '''
    ''' Interlace sentence with numbers '''
    original_tokens = sentence.split(" ")
    number_tokens, idcs = find_continugous_number_words(original_tokens)
    print(number_tokens)
    print(idcs)

    output_tokens = []

    if len(number_tokens) != 0:
        number_tokens_counter = 0
        idx = 0
        while idx < len(original_tokens):
            if number_tokens_counter < len(number_tokens) and idx == idcs[number_tokens_counter][0]:
                output_tokens.append(parse_number_word(number_tokens[number_tokens_counter]))
                idx = idcs[number_tokens_counter][1]
                number_tokens_counter += 1
            else:
                output_tokens.append(original_tokens[idx])
                idx += 1
    else:
        output_tokens = original_tokens
    return ' '.join(output_tokens)


print(text2int("one thousand three hundred people went to three million twelve stores and two billion one thousand stores"))