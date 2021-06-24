import re
import time
import string 
import calendar
import datetime
import numpy as np
import phonenumbers
from num2words import num2words
from phonenumbers import carrier, timezone, geocoder
from supplements import symbol_to_currency_name_dict, TimeInWords2, abbreviated_currency_symbols_to_currency_name_dict

### Recognizers

def recognized_as_datestring(x):
    """
    As per formats listed in the https://en.wikipedia.org/wiki/Date_format_by_country, accepting:
    
    x = '2018-25-12'
    x = '2018-12-25'
    x = '25-12-2018'

    x = '18/25/12'
    x = '18/12/25'
    x = '25/12/18'
    
    Accepting also the separator -, ., :, /
    """
    x = re.sub('[.:/]', '-', x)
    
    try:
        datetime_x = datetime.datetime.strptime(x, '%m-%d-%Y')
        return True, datetime_x
    except ValueError:
        try:
            datetime_x = datetime.datetime.strptime(x, '%d-%m-%Y')
            return True, datetime_x
        except ValueError:
            try:
                datetime_x = datetime.datetime.strptime(x, '%Y-%m-%d')
                return True, datetime_x
            except ValueError:
                    try:
                        datetime_x = datetime.datetime.strptime(x, '%m-%d-%y')
                        return True, datetime_x
                    except ValueError:
                        try:
                            datetime_x = datetime.datetime.strptime(x, '%d-%m-%y')
                            return True, datetime_x
                        except ValueError:
                            try:
                                datetime_x = datetime.datetime.strptime(x, '%y-%m-%d')
                                return True, datetime_x
                            except ValueError:
                                return False, False

def recognized_as_year(x):
    possible_year_list = [str(x) for x in np.arange(1,2090,1)]

    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()
        
    after_assumed_year = x[end_digit_index:]
    before_assumed_year = x[:begin_digit_index]
    year = x[begin_digit_index:end_digit_index]
    
    checker = min([character in string.punctuation for character in after_assumed_year]+[True]) and \
              min([character in string.punctuation for character in before_assumed_year]+[True]) and \
              year in possible_year_list and (len(year) <= 4) and year.isnumeric()
    if checker:
        return bool(re.compile(r'.*([1-3][0-9]{3})').match(x))
    else:
        return False

def recognized_as_time(x):
    try:
        time.strptime(x, '%H:%M')
        return True
    except ValueError:
        try:
            time.strptime(x, '%H.%M')
            return True
        except ValueError:
            return False

def recognized_as_phone_number(x):
    """
    Using https://github.com/daviddrysdale/python-phonenumbers,
    a Python port of Google's libphonenumber library 
    
    Accepting VALID phone number format EVEN WITH STRIPES IN BETWEEN
    This function also do a check on the number whether it's a valid phone number or not
    (can't accept a random phone number here)
    phone_number = "+62-87986-123456"
    """
    try:
        my_number = phonenumbers.parse(x, None)
        return phonenumbers.is_valid_number(my_number)
    except:
        return False

def recognized_as_currency_symbols(x):
    """
    # x = '$300US' # False
    # x = '$300!@#' # False
    # x = '300!@#' # False
    # x = '!@#300$' # False
    # x = '300US' # False

    # x = '$300' # True
    # x = '300$' # True
    # x = 'USD300' # True
    # x = '300USD' # True
    """
    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    currency_symbols = list(symbol_to_currency_name_dict.keys())
    currency_abbreviations = list(abbreviated_currency_symbols_to_currency_name_dict.keys())

    if x[:begin_digit_index] in currency_symbols:
        other_end_non_numeric = x[begin_digit_index:][end_digit_index-(len(x[:begin_digit_index])):]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif x[:begin_digit_index] in currency_abbreviations:
        other_end_non_numeric = x[begin_digit_index:][end_digit_index-(len(x[:begin_digit_index])):]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif x[end_digit_index:] in currency_symbols:
        other_end_non_numeric = x[:begin_digit_index]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif x[end_digit_index:] in currency_abbreviations:
        other_end_non_numeric = x[:begin_digit_index]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    else:
        return False

def recognized_as_long_number(x):
    if x[0] == '+':
        x = x[1:]
    
    threshold = 7
    return len(x) >= threshold and x.isnumeric()

def recognized_as_general_numbers(x):
    return x.isnumeric()
    
### Transformers

def datestring_to_words(x):
    words = num2words(x.day, to='ordinal') + ' of ' + calendar.month_name[x.month].lower() + ' ' + year_to_words(str(x.year))
    return words

def time_to_words(x):
    """
    Currently accepted time formats are:
    - x = "10x30" with x being any non integer our-minute separator
    - 12h formats (e.g. 24:00 = twelve o'clock, 30:00 = eighteen o'clock)
    
    Possible but not yet catered time formats:
    - Timestamps
    """
    t = TimeInWords2()
    words = t.caltime(x)
    return words

def year_to_words(x):
    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    after_assumed_year = x[end_digit_index:]
    before_assumed_year = x[:begin_digit_index]
    year = x[begin_digit_index:end_digit_index]

    year_word = ''.join(num2words(year, to='year').split(","))
    words = "".join([before_assumed_year, year_word, after_assumed_year])
    return words

def phonenum_to_words(x):
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    
    if '+' in x:
        if x.index('+') == 0:
            words = 'plus '
    else:
        words = ''
    
    x = re.sub("[^0-9]", "", x)
    for number in x:
        words = words + numbers[int(number)] + ' '
    return words

def currency_to_words(x):
    currency_symbols = list(symbol_to_currency_name_dict.keys())
    currency_abbreviations = list(abbreviated_currency_symbols_to_currency_name_dict.keys())

    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    if x[:begin_digit_index] in currency_symbols: #$300
        number = re.sub("[^0-9]", "", x[begin_digit_index:])
        money = ''.join(num2words(number).split(","))
        currency = str.lower(symbol_to_currency_name_dict[x[:begin_digit_index]])
        words = money + ' ' + currency
    elif x[:begin_digit_index] in currency_abbreviations: #USD300
        number = re.sub("[^0-9]", "", x[begin_digit_index:])
        money = ''.join(num2words(number).split(","))
        currency = str.lower(abbreviated_currency_symbols_to_currency_name_dict[x[:begin_digit_index]])
        words = money + ' ' + currency
    elif x[end_digit_index:] in currency_symbols: #300$
        number = re.sub("[^0-9]", "", x[:end_digit_index])
        money = ''.join(num2words(number).split(","))
        currency = str.lower(symbol_to_currency_name_dict[x[end_digit_index:]])
        words = money + ' ' + currency
    elif x[end_digit_index:] in currency_abbreviations: #300USD
        number = re.sub("[^0-9]", "", x[:end_digit_index])
        money = ''.join(num2words(number).split(","))
        currency = str.lower(abbreviated_currency_symbols_to_currency_name_dict[x[end_digit_index:]])
        words = money + ' ' + currency
    return words

def long_number_to_word(x):
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    
    if x[0] == '+':
        x = x[1:]
        words = 'plus '
    else:
        words = ''
        
    for number in x:
        words = words + numbers[int(number)] + ' '
    return words

def general_numbers_to_words(x):
    """
    General number and decimals (Distance, weight, etc)
    """
    words = ''.join(num2words(x).split(","))
    return words
    
### Implementations 

def recognize_transform(token):
    if bool(re.search(r'\d', token)):
        datestring_recognized, new_token = recognized_as_datestring(token)
        if type(new_token) != bool:
            token = new_token
            
        if datestring_recognized:
            words = datestring_to_words(token)
            return words
        elif recognized_as_time(token):
            words = time_to_words(token)
            return words
        elif recognized_as_year(token):
            words = year_to_words(token)
            return words
        elif recognized_as_currency_symbols(token):
            words = currency_to_words(token)
            return words
        elif recognized_as_phone_number(token): 
            words = phonenum_to_words(token)
            return words
        elif recognized_as_long_number(token):
            words = long_number_to_word(token)
            return words
        elif recognized_as_general_numbers(token):
            words = general_numbers_to_words(token)
            return words
        else: # ELSE: Numbers that not in the above stated formats, strings
            return token
    else:
        return token