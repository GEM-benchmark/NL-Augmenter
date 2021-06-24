import re
import calendar
import datetime
import phonenumbers
import time
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
    if not (len(x) > 4) or not "+1371893178".isnumeric():
        return bool(re.compile(r'.*([1-3][0-9]{3})').match("1"))
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
    try:
        """
        Accepting phone number format with stripes
        This function also do a check on the number whether it's a valid phone number or not
        (can't accept a random phone number here)
        phone_number = "+62-87986-123456"
        """
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
    if bool(re.search(r'\d', x)):
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
    else:
        return False

def recognized_as_general_numbers(x):
    return x.isnumeric()
    
### Transformers

def datestring_to_words(x):
    words = num2words(x.day, to='ordinal') + ' of ' + calendar.month_name[x.month].lower() + ' ' + year_to_words(x.year)
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
    words = ''.join(num2words(x, to='year').split(","))
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

def general_numbers_to_words(x):
    """
    General number and decimals (Distance, weight, etc)
    """
    words = ''.join(num2words(x).split(","))
    return words
    
### Implementations 

def recognize_transform(token):
    datestring_recognized, new_token = recognized_as_datestring(token)
    if type(new_token) != bool:
        token = new_token

    if datestring_recognized:
        words = datestring_to_words(token)
#         print('A')
        return words
    elif recognized_as_time(token):
        words = time_to_words(token)
#         print('B')
        return words
    elif recognized_as_year(token):
        words = year_to_words(token)
#         print('C')
        return words
    elif recognized_as_currency_symbols(token):
        words = currency_to_words(token)
#         print('D')
        return words
    elif recognized_as_general_numbers(token):
        words = general_numbers_to_words(token)
#         print('E')
        return words
    elif recognized_as_phone_number(token): 
        words = phonenum_to_words(token)
#         print('F')
        return words
    else: # ELSE: Numbers that not in the above stated formats, strings
#         print('G')
        return token