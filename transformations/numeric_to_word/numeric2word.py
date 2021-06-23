import re
import calendar
import datetime
import phonenumbers
from num2words import num2words
from phonenumbers import carrier, timezone, geocoder
from supplements import symbol_to_currency_name_dict, TimeInWords2

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
    return bool(re.compile(r'.*([1-3][0-9]{3})').match(x))

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
    Accepting phone number format with stripes
    This function also do a check on the number whether it's a valid phone number or not
    (can't accept a random phone number here)
    phone_number = "+62-87986-123456"
    """
    my_number = phonenumbers.parse(x, "ID")
    return phonenumbers.is_valid_number(my_number)

def recognized_as_currency_symbols(x):
    return x in list(symbol_to_currency_name_dict.keys())

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
    
    x = re.sub("[^0-9]", "", x)
    
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

def numeric2word(token):
    datestring_recognized, token = recognized_as_datestring(token)
    if datestring_recognized:
        words = datestring_to_words(token)
        return words
    elif recognized_as_time(token):
        words = time_to_words(token)
        return words
    elif recognized_as_year(token):
        words = year_to_words(token)
        return words
    elif recognized_as_phone_number(token): 
        words = phonenum_to_words(token)
        return words
    elif recognized_as_currency_symbols(token):
        words = symbol_to_currency_name_dict[token]
        return words
    elif recognized_as_general_numbers(token):
        words = general_numbers_to_words(token)
        return words
    else: # ELSE: Numbers that not in the above stated formats, strings
        return token