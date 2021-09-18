'''
Very loosely adapted from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
'''

import re

from words_to_numbers_constants import units, tens, teens, scales

def period_rep(tokens, period_start_loc, period_end_loc):
    """
    Parse a "period" of the number corresponding to 3 digits, given a sequence of tokens and the location of the period
    in that sentence
    """
    str_ = ''

    first_digit = '0'
    if 'hundred' in tokens[period_start_loc:period_end_loc]:
        # The token before "hundred" must be the "number of hundreds"
        hundred_idx = tokens.index('hundred')
        first_digit = units[tokens[hundred_idx - 1]]  # Will raise KeyError if malformed input
        period_start_loc += 2 # Now, only consider tokens after the "X hundred" in the sequence
    str_ += first_digit

    second_digit = '0'
    for t in tens:
        if t in tokens[period_start_loc:period_end_loc]:
            second_digit = tens[t]
            period_start_loc += 1 # Now, only consider tokens after the tens quantifier in the sequence
    str_ += second_digit

    third_digit = '0'
    for u in units:
        if u in tokens[period_start_loc:period_end_loc]:
            third_digit = units[u]
            period_start_loc += 1 # Though this is not used currently, leave it here for extensions like "one point six"
    str_ += third_digit

    # Handle the case of 11 - 19
    for te in teens:
        if te in tokens[period_start_loc:period_end_loc]:
            str_ = str_[0] + teens[te] # Can't do in-place because of 'str' object does not support item assignment

    return str_

def is_token_numeric(token):
    """
    Decide if a given token is part of the number
    """
    return token != ',' and (token in units or token in tens or token in scales or token == 'hundred' or token in teens)

def find_continugous_number_words(tokens):
    """
    Given all the tokens of a sentence, find all the phrases that correspond to words.
    This is necessary because several "word numbers" may be present in a sentence, e.g.
    'three hundred people went to twenty two events'

    Returns a set of "word numbers" and their corresponding start and end indices in the original token sequence
    """
    number_words = []
    start_idcs = []
    end_idcs = []

    t_idx = 0
    new_word = True
    while t_idx < len(tokens):
        if is_token_numeric(tokens[t_idx]): # BUG: What about commas and hyphens and "and"?
            if new_word: # We've found a new "word number"
                start_idx = t_idx
                start_idcs.append(t_idx)
                new_word = False
        else:
            if not new_word: # We just completed the "word number"
                number_words.append(tokens[start_idx:t_idx])
                end_idcs.append(t_idx)
            new_word = True
        t_idx += 1

    return number_words, list(zip(start_idcs, end_idcs))

def parse_number_word(number_tokens):
    """
    Given a sequence of tokens corresponding to a "word number", converts it to a decimal representation, e.g.
    'Three thousand five hundred twelve' -> '3512'
    """
    word_rep = ' '.join(number_tokens)
    word_rep = word_rep.replace('-', ' ')
    word_rep = word_rep.replace(' and ', ' ')
    tokens = re.split('( |,)', word_rep)
    tokens = list(filter(lambda x: x != ' ' and x != '', tokens)) # Remove extraneous empty strings and spaces

    num_string = ''
    last_found_period = None

    # Search the possible period identifiers backwards to look for biggest scale first.
    # As of Python 3.6, for the CPython implementation of Python, dictionaries maintain insertion order by default.
    for period in list(scales)[::-1]:
        if period in tokens:

            # We found a new period identifier and had an old one that wasn't the one immediately larger than it,
            # so we need to pad the middle with zeros, e.g. in the number "one billion, one thousand one"
            if last_found_period is not None:
                num_string += '0' * 3 * (list(scales).index(last_found_period) - list(scales).index(period) - 1)

            last_found_period = period
            period_end_loc = tokens.index(period)

            # We need to find the tokens that correspond to the period under identification.
            # Walk backwards to find comma or non-number word
            period_start_loc = period_end_loc - 1
            token = tokens[period_start_loc]
            # Walk back towards the last seen period identifier like million, billion, etc. and
            # don't wrap back around around the string
            while is_token_numeric(token) and token not in scales and period_start_loc != 0:
                period_start_loc -= 1
                token = tokens[period_start_loc]

            num_string += period_rep(tokens, period_start_loc, period_end_loc)

    # Handle the corner cases like "one million and twelve"
    if last_found_period is not None and last_found_period != 'thousand':
        num_string += '0' * 3 * (list(scales).index(last_found_period))

    # Trim leading 0s
    num_string = num_string.lstrip('0')

    # If the last token is not a period identifier, then we have a number less than one thousand
    if last_found_period is None:
        num_string += period_rep(tokens, 0, len(tokens))
    elif tokens.index(last_found_period) != len(scales):
        num_string += period_rep(tokens, tokens.index(last_found_period)+1, len(tokens))
    else:
        num_string += '0' * scales[last_found_period] # Add right-zeros in the case we had a number like "one million"

    return num_string


def text2int(sentence):
    """
    Given a sentence, find the contiguous subsequences of tokens that correspond to a number.
    Convert those to their decimal representations, and interlace them with the original sentence.
    """
    output_tokens = []
    original_tokens = sentence.split(" ")
    number_tokens, idcs = find_continugous_number_words(original_tokens)

    if len(number_tokens) != 0: # We have some numbers to convert
        number_tokens_counter = 0
        idx = 0
        while idx < len(original_tokens):
            if number_tokens_counter < len(number_tokens) and idx == idcs[number_tokens_counter][0]: # Number to convert
                output_tokens.append(parse_number_word(number_tokens[number_tokens_counter]))
                idx = idcs[number_tokens_counter][1] # Skip ahead to the end of the word number
                number_tokens_counter += 1
            else: # Keep original tokens
                output_tokens.append(original_tokens[idx])
                idx += 1
    else:
        output_tokens = original_tokens
    return ' '.join(output_tokens)

# BUG: Capitalization
print(text2int("one thousand three hundred people went to three million twelve stores and two billion one thousand stores"))