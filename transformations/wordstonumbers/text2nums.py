import re

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
    # parse period
    str_ = ''

    first_digit = '0'
    if 'hundred' in tokens[period_start_loc:period_end_loc]:
        # The token before "hundred" must be the number of hundreds
        hundred_idx = tokens.index('hundred')
        first_digit = units[tokens[hundred_idx - 1]]  # Should raise KeyError if malformed input
    str_ += first_digit

    second_digit = '0'
    for t in tens:
        if t in tokens[period_start_loc:period_end_loc]:
            second_digit = tens[t]
    str_ += second_digit

    third_digit = '0'
    for u in units:
        if u in tokens[period_start_loc:period_end_loc]:
            third_digit = units[u]
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
    number_word_idcs = []

    t_idx = 0
    new_word = True
    while t_idx < len(tokens):
        if is_token_numeric(tokens[t_idx]): # What about commas and hyphens and "and"?
            if new_word:
                start_idx = t_idx
                number_word_idcs.append(t_idx)
                new_word = False
        else:
            if not new_word:
                number_words.append(tokens[start_idx:t_idx])
            new_word = True
        t_idx += 1

    return number_words, number_word_idcs

def parse_number_word(number_tokens):
    # If there's a hyphen, split
    word_rep = ' '.join(number_tokens)
    word_rep = word_rep.replace('-', ' ')
    word_rep = word_rep.replace('and ', '')
    # Split by space
    tokens = re.split('( |,)', word_rep)
    tokens = list(filter(lambda x: x != ' ' and x != '', tokens))

    num_string = ''
    # If there's an and, split

    last_found_period = None
    for period in list(scales)[::-1]:  # Do them backwards to look for biggest scale first
        if period in tokens:
            last_found_period = period
            period_end_loc = tokens.index(period)

            # walk backwards to find comma or non-number word
            period_start_loc = period_end_loc
            token = tokens[period_start_loc]
            while is_token_numeric(token):
                period_start_loc -= 1
                if period_start_loc == 0:  # Don't wrap around the string
                    break
                token = tokens[period_start_loc]

            num_string += period_rep(tokens, period_start_loc, period_end_loc)

    # Trim leading 0s
    num_string = num_string.lstrip('0')

    # Add right-zeros in the case we had a number like "one million"
    num_string += '0' * scales[last_found_period]
    return num_string


def text2int(textnum):
    '''
    Loosely adapted from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
    '''

    # Bugs: Need to include last period

    number_tokens, start_idx = find_continugous_number_words("one thousand people went to three million stores and two billion stores".split(" "))
    print(parse_number_word(number_tokens[0]))
    print(parse_number_word(number_tokens[1]))
    print(parse_number_word(number_tokens[2]))
    # print(find_continugous_number_words("one hundred people went to three thousand stores and two hundred stores".split(" ")))
    # print(text2int("seven billion, a hundred twelve million, thirty one thousand, three hundred thirty seven"))


text2int('')