import re
import time
import string 
import calendar
import datetime
import numpy as np
import phonenumbers
from num2words import num2words
from unidecode import unidecode
from phonenumbers import carrier, timezone, geocoder

special_numbers = ['911']

### Recognizers

def recognized_as_power_of_ten(word, prev_word):
    return word[:2] == '10' and unidecode(prev_word) == 'x'

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

def recognized_as_incomplete_date(x):
    """
    As per formats listed in the https://en.wikipedia.org/wiki/Date_format_by_country, accepting:
    
    x = '01/2020'
    x = '2020/01'
    x = '20/01'
    x = '01/20'
    
    Accepting only the separator /
    """
    
    try:
        datetime_x = datetime.datetime.strptime(x, '%Y/%m')
        return True, datetime_x
    except ValueError:
        try:
            datetime_x = datetime.datetime.strptime(x, '%y/%m')
            return True, datetime_x
        except ValueError:
            try:
                datetime_x = datetime.datetime.strptime(x, '%m/%Y')
                return True, datetime_x
            except ValueError:
                try:
                    datetime_x = datetime.datetime.strptime(x, '%m/%y')
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

    if x.find('.') > -1:
        front_checker = x[:begin_digit_index-1]
    else:
        front_checker = x[:begin_digit_index]
    
    if x.find('.') > -1:
        back_checker = x[end_digit_index:]
    else:
        back_checker = x[end_digit_index:]
    
    if front_checker in currency_symbols:
        other_end_non_numeric = x[begin_digit_index:][end_digit_index-(len(x[:begin_digit_index])):]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif front_checker in currency_abbreviations:
        other_end_non_numeric = x[begin_digit_index:][end_digit_index-(len(x[:begin_digit_index])):]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif back_checker in currency_symbols:
        if x.find('.') > -1:
            other_end_non_numeric = x[:begin_digit_index-1]
        else:
            other_end_non_numeric = x[:begin_digit_index]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    elif back_checker in currency_abbreviations:
        if x.find('.') > -1:
            other_end_non_numeric = x[:begin_digit_index-1]
        else:
            other_end_non_numeric = x[:begin_digit_index]
        return other_end_non_numeric in currency_symbols or other_end_non_numeric in currency_abbreviations or len(other_end_non_numeric) == 0
    else:
        return False
    
def recognized_as_cents(x):
    return ('¢' in x or x[-1] == 'c') and x[-2].isnumeric() and re.sub('[¢c,.]', "", x).isnumeric()

def recognized_as_long_number(x):
    if x[0] == '+':
        x = x[1:]
    
    threshold = 7
    return len(x) >= threshold and x.isnumeric()

def recognized_as_long_number_with_stripes(x):
    return len(re.sub('[0-9-]','',x)) == 0 and len(x) > 8

def recognized_as_sticky_numbers(x):
    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    first_part = x[begin_digit_index:end_digit_index]
    last_part = x[end_digit_index:]
    return re.search(r'^\d*[.,]?\d*$',first_part) and (last_part in ['st', 'nd', 'rd','th', '%'] or not re.search(r'\d', last_part)) and x[0].isnumeric()

def recognized_as_math_formula_equality(x):
    matches = []
    for equality_sign in ['=', '<', '<=', '=>', '>', '!=']:
        if equality_sign in x and x.count(equality_sign) == 1:
            matches.append(True)
        else:
            matches.append(False)
    return sum(matches)>0

def recognize_numeric_in_begin_end_bracket(x):
    is_bracketed = (x[0] == '(' and x[-1] == ')') or\
                   (x[0] == '[' and x[-1] == ']') or\
                   (x[0] == '{' and x[-1] == '}') or\
                   (x[0] == '<' and x[-1] == '>')
    return is_bracketed

def recognized_as_math_bracket(x):
    return x[0] == '(' and recognized_as_sticky_numbers(x[1:])

def recognized_as_special_phone_number(x):
    return x[0] in '*#' and x[-1] in '*#'

def recognized_as_general_numbers(x):
    return x.replace(',','').replace('.','').isnumeric() and x[-1].isnumeric()

def recognized_as_special_numbers(x):
    return x in special_numbers
    
### Transformers

def datestring_to_words(x):
    words = 'the ' + num2words(x.day, to='ordinal') + ' of ' + calendar.month_name[x.month].lower() + ' ' + year_to_words(str(x.year))
    return words

def incompelete_date_to_words(x):
    words = calendar.month_name[x.month].lower() + ' ' + year_to_words(str(x.year))
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
        if x.index('+') == 0 or x.index('+') == 1:
            words = 'plus '
    else:
        words = ''
    
    x = re.sub("[^0-9]", "", x)
    for i, number in enumerate(x):
        if i == len(x)-1:
            words = words + numbers[int(number)]
        else:
            words = words + numbers[int(number)] + ' '
    return words

def currency_to_words(x):
    currency_symbols = list(symbol_to_currency_name_dict.keys())
    currency_abbreviations = list(abbreviated_currency_symbols_to_currency_name_dict.keys())

    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()
    
    front_checker = re.sub("[.]", "", x[:begin_digit_index])
    back_checker = x[end_digit_index:]

    if front_checker in currency_symbols: # $300
        if x.find('.') > -1:
            number = re.sub("[^.0-9]", "", x[begin_digit_index-1:])
            currency = str.lower(symbol_to_currency_name_dict[re.sub("[.]", "", x[:begin_digit_index])])
            if len(number[number.index('.')+1:]) > 0 and len(number[:number.index('.')])==0:
                if int(number[number.index('.')+1:]) > 1:
                    words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cents'
                elif int(number[number.index('.')+1:]) == 1:
                    words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cent'
            else:
                words = num2words(number) + ' ' + currency       
        else:
            number = re.sub("[^.0-9]", "", x[begin_digit_index:])
            currency = str.lower(symbol_to_currency_name_dict[re.sub("[.]", "", x[:begin_digit_index])])
            words = num2words(number) + ' ' + currency
    elif front_checker in currency_abbreviations: # USD300
        if x.find('.') > -1:
            number = re.sub("[^.0-9]", "", x[begin_digit_index-1:])
            currency = str.lower(abbreviated_currency_symbols_to_currency_name_dict[re.sub("[.]", "", x[:begin_digit_index])])
            if len(number[number.index('.')+1:]) > 0 and len(number[:number.index('.')])==0:
                if int(number[number.index('.')+1:]) > 1:
                    words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cents'
                elif int(number[number.index('.')+1:]) == 1:
                    words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cent'
            else:
                words = num2words(number) + ' ' + currency   
        else:
            number = re.sub("[^.0-9]", "", x[begin_digit_index:])
            currency = str.lower(abbreviated_currency_symbols_to_currency_name_dict[re.sub("[.]", "", x[:begin_digit_index])])
            words = num2words(number) + ' ' + currency
    elif back_checker in currency_symbols: # 300$
        number = re.sub("[^.0-9]", "", x[:end_digit_index])
        currency = str.lower(symbol_to_currency_name_dict[x[end_digit_index:]])
        if number.find('.') > -1 and len(number[number.index('.')+1:]) > 0 and len(number[:number.index('.')])==0:
            if int(number[number.index('.')+1:]) > 1:
                words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cents'
            elif int(number[number.index('.')+1:]) == 1:
                words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cent'
        else:
            words = num2words(number) + ' ' + currency
    elif back_checker in currency_abbreviations: # 300USD
        number = re.sub("[^.0-9]", "", x[:end_digit_index])     
        currency = str.lower(abbreviated_currency_symbols_to_currency_name_dict[x[end_digit_index:]])
        if number.find('.') > -1 and len(number[number.index('.')+1:]) > 0 and len(number[:number.index('.')])==0:
            if int(number[number.index('.')+1:]) > 1:
                words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cents'
            elif int(number[number.index('.')+1:]) == 1:
                words = num2words(number[number.index('.')+1:]) + ' ' + currency + ' cent'
        else:
            words = num2words(number) + ' ' + currency
    return words

def cents_to_words(x):
    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    first_part = x[begin_digit_index:end_digit_index]

    return num2words(first_part) + ' cents'

def long_number_to_words(x):
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    
    if x[0] == '+':
        x = x[1:]
        words = 'plus '
    else:
        words = ''
        
    for i, number in enumerate(x):
        if i == len(x)-1:
            words = words + numbers[int(number)]
        else:
            words = words + numbers[int(number)] + ' '
    return words

def long_number_with_stripes_to_words(x):
    words = ''
    for i, char in enumerate(x):
        if char.isnumeric():
            if i == len(x)-1:
                words = words + num2words(char) 
            else:
                words = words + num2words(char) + ' '
        else:
            if i == len(x)-1:
                words = words + char 
            else:
                words = words + char + ' '
    return words

def sticky_numbers_to_words(x):

    begin_digit_index = re.search(r"\d", x).start()
    end_digit_index = len(x) - re.search(r"\d", x[::-1]).start()

    first_part = x[begin_digit_index:end_digit_index]
    last_part = x[end_digit_index:]

    if last_part in ['st', 'nd', 'rd', 'th']:
        words = num2words(first_part, to='ordinal')
    else:
        words = num2words(first_part, to='cardinal') + ' ' +  last_part if len(last_part) > 0 else num2words(first_part, to='cardinal')
    return words

def math_formula_equality_to_words(x):
    equality_sign_index_list = []
    for equality_sign in ['=', '<', '<=', '=>', '>', '!=']:
        equality_sign_index_list.append(x.find(equality_sign))
    
    equality_sign_index_numpy = np.array(equality_sign_index_list)
    count_match = sum(equality_sign_index_numpy > 0)
    if count_match > 1:
        equality_sign_index = max(equality_sign_index_numpy)
    elif count_match == 1:
        equality_sign_index = list(equality_sign_index_numpy > 0).index(True)
        
    equality_sign = ['=', '<', '<=', '=>', '>', '!='][equality_sign_index]
    
    begin_equality_sign_index_in_word = x.index(equality_sign)
    end_equality_sign_index_in_word = x.index(equality_sign)+len(equality_sign)

    before_equal = x[:begin_equality_sign_index_in_word]
    after_equal = x[end_equality_sign_index_in_word:]

    begin_digit_index = re.search(r"\d", after_equal).start()
    end_digit_index = len(after_equal) - re.search(r"\d", after_equal[::-1]).start()

    first_part = after_equal[begin_digit_index:end_digit_index]
    last_part = after_equal[end_digit_index:]

    after_equal = num2words(first_part) + ' ' +  last_part

    words = before_equal + ' ' + equality_sign + ' ' + after_equal
    return words

def math_bracket_to_words(x):
    return '( ' + sticky_numbers_to_words(x[1:])

def general_numbers_to_words(x):
    """
    General number and decimals (Distance, weight, etc)
    """
    if ',' in x:
        # find the last_comma_till_the_end_of_numerical_char_after_last_comma
        last_comma_index = max([i for i, ltr in enumerate(x) if ltr == ','])

        count = 0
        for i in np.arange(last_comma_index+1, len(x), 1):
            if x[i].isnumeric():
                count = count + 1
            else:
                break

        if count == 3:
            # last comma until the first comma is not needed
            x = x.replace(',','')

        if count != 3:
            # last comma is actually dot, there'll only 1 comma in this case
            x = x[:last_comma_index] + '.' + x[last_comma_index+1:]
        
    words = ''.join(num2words(x).split(","))
    return words
    
### Implementations 

def recognize_transform(word, prev_word, next_word):
    
    if recognized_as_power_of_ten(word, prev_word):
        words = 'ten power ' + num2words(unidecode(word[2:]))
        return words
    elif bool(re.search(r'\d', word)):
        datestring_recognized, new_dateword = recognized_as_datestring(word)
        incomplete_date_recognized, new_incomplete_date_word = recognized_as_incomplete_date(word)
        if type(new_incomplete_date_word) != bool:
            word = new_incomplete_date_word
        elif type(new_dateword) != bool:
            word = new_dateword

        if datestring_recognized:
            words = datestring_to_words(word)
#             print('A', word, words)
            return words
        elif incomplete_date_recognized:
            words = incompelete_date_to_words(word)
#             print('B', word, words)
            return words
        elif recognized_as_special_numbers(word):
            words = phonenum_to_words(word)
#             print('C', word, words)
            return words
        elif recognized_as_general_numbers(word):
            words = general_numbers_to_words(word)
#             print('D', word, words)
            return words
        elif recognized_as_time(word):
            words = time_to_words(word)
#             print('E', word, words)
            return words
        elif recognized_as_year(word):
            words = year_to_words(word)
#             print('F', word, words)
            return words
        elif recognized_as_currency_symbols(word):
            words = currency_to_words(word)
#             print('G', word, words)
            return words
        elif recognized_as_cents(word):
            words = cents_to_words(word)
#             print('H', word, words)
            return words
        elif recognized_as_phone_number(word): 
            words = phonenum_to_words(word)
#             print('I', word, words)
            return words
        elif recognized_as_special_phone_number(word):
            words = word[0] + ' ' + phonenum_to_words(word) + ' ' + word[-1]
#             print('J', word, words)
            return words
        elif recognized_as_long_number(word):
            words = long_number_to_words(word)
#             print('K', word, words)
            return words
        elif recognized_as_long_number_with_stripes(word):
            words = long_number_with_stripes_to_words(word)
#             print('L', word, words)
            return words
        elif recognized_as_sticky_numbers(word):
            words = sticky_numbers_to_words(word)
#             print('M', word, words)
            return words
        elif recognized_as_math_formula_equality(word):
            words = math_formula_equality_to_words(word)
#             print('N', word, words)
            return words
        elif recognize_numeric_in_begin_end_bracket(word):
            words = word[0] + recognize_transform(word[1:-1], ' ', ' ') + word[-1]
#             print('O', word, words)
            return words
        elif recognized_as_math_bracket(word):
            words = math_bracket_to_words(word)
#             print('P', word, words)
            return words
        else: # ELSE: Numbers that not in the above stated formats, strings
#             print('Q', word)
            return word
    else:
#         print('R', word)
        return word

### Supplements

class TimeInWords2():
    def __init__(self):
        self.words=["one", "two", "three", "four", "five", "six", "seven", "eight","nine", 
       "ten", "eleven", "twelve", "thirteen", "fourteen", "quarter", "sixteen",
       "seventeen", "eighteen", "nineteen", "twenty", "twenty one", 
       "twenty two", "twenty three", "twenty four", "twenty five", 
       "twenty six", "twenty seven", "twenty eight", "twenty nine", "half"]
         
    def caltime(self, time_string):
        splitter = ''.join([i for i in time_string if not i.isdigit()])
        hrs = int(time_string.split(splitter)[0])
        mins = int(time_string.split(splitter)[1])
        header = "" #It is..
        msg=""
        am_pm = "am"
        if (hrs >12):
            hrs=hrs-12
            am_pm = "pm"
        if (mins == 0):
            hr = self.words[hrs-1]
            msg=header + hr + " o'clock" + " " + am_pm #+ "."
        elif (mins < 31):      
               hr = self.words[hrs-1]
               mn = self.words[mins-1]
               msg = header + mn + " past " + hr + " " + am_pm #+ "."
        else:
            hr = self.words[hrs]
            mn =self.words[(60 - mins-1)]
            msg = header + mn + " to " + hr + " " + am_pm #+ "."
        return msg
    
symbol_to_currency_name_dict = {"؋":"Afghanistani Afghani", 
                                "₼":"Azerbaijani Manat",
                                ".د.ب":"Bahraini Dinar",
                                "৳":"Bangladeshi Taka",
                                "Nu.":"Bhutanese Ngultrum",
                                "$":"Dollar",
                                "៛":"Cambodian Riel",
                                "¥":"Chinese Yuan Renminbi", # Can also be"¥":"Japanese Yen"
                                "ლ":"Georgian Lari",
                                "₹":"Indian Rupee",
                                "Rp":"Indonesian Rupiah",
                                "﷼":"Iranian Rial",
                                "ع.د":"Iraqi Dinar",
                                "₪":"Israeli New Sheqel",
                                "د.ا":"Jordanian Dinar",
                                "лв":"Kazakhstani Tenge",
                                "د.ك":"Kuwaiti Dinar",
                                "лв":"Kyrgyzstani Som",
                                "₭":"Lao Kip",
                                "RM":"Malaysian Ringgit",
                                "Rf":"Maldives Rufiyaa",
                                "₮":"Mongolian Tugrik",
                                "K":"(Burma) Myanmar Kyat",
                                "₨":"Nepalese Rupee", 
                                "₩":"North Korean Won",
                                "﷼":"Omani Rial",
                                "₨":"Pakistan Rupee",
                                "د.ا":"Jordanian Dinar",
                                "₱":"Philippine Peso",
                                "﷼":"Qatari Riyal",
                                "₽":"Russian Ruble",
                                "﷼":"Saudi Arabian Riyal",
                                "₩":"Korean Won",
                                "₨":"Sri Lankan Rupee",
                                "NT$":"New Taiwan Dollar",
                                "ЅM":"Tajikistan Somoni",
                                "฿":"Thai Baht",
                                "₺":"Turkish New Lira",
                                "T":"Turkmenistani Manat",
                                "د.إ":"United Arab Emirates Dirham",
                                "лв":"Uzbekistani Som",
                                "₫":"Viet Nam Dong",
                                "﷼":"Yemeni Rial",
                                "دج":"Algerian Dinar",
                                "Kz":"Angolan Kwanza",
                                "P":"Botswana Pula",
                                "FBu":"Burundian Franc",
                                "FCFA":"Central African CFA",
                                "CF":"Comorian Franc",
                                "FC":"Congolese franc",
                                "Fdj":"Djiboutian Franc",
                                "ናቕፋ":"Eritrean Nakfa",
                                "ብር":"Ethiopian Birr",
                                "D":"Gambian Dalasi",
                                "GH₵":"Ghanaian Cedi",
                                "FG":"Guinean Franc",
                                "KSh,":"Kenyan Shilling",
                                "L":"Lesotho Loti",
                                "ل.د":"Libyan Dinar",
                                "Ar":"Malagasy Ariary",
                                "MK":"Malawian Kwacha",
                                "UM":"Mauritanian Ouguiya",
                                "₨":"Mauritian Rupee",
                                "DH":"Moroccan Dirham",
                                "MT":"Mozambican Metical",
                                "₦":"Nigerian Naira",
                                "FRw":"Rwandan Franc",
                                "Db":"Sao Tome Dobra",
                                "CFA":"West African CFA",
                                "₨":"Seychelles Rupee",
                                "Le":"Sierra Leonean Leone",
                                "S":"Somali Shilling",
                                "R":"South African Rand",
                                "SD":"Sudanese pound",
                                "E":"Swazi Lilangeni",
                                "TSh":"Tanzanian Shilling",
                                "د.ت":"Tunisian Dinar",
                                "USh":"Ugandan Shilling",
                                "ZK":"Zambian Kwacha",
                                "Lek":"Albanian Lek",
                                "€":"Euro",
                                "դր.":"Armenian Dram",
                                "₼":"Azerbaijani Manat",
                                "Br":"Belarusian Ruble",
                                "KM":"Bosnia-Herzegovina Convertible Mark",
                                "лв":"Bulgarian Lev",
                                "kn":"Croatian Kuna",
                                "Kč":"Czech Koruna",
                                "kr.":"Danish Krone",
                                "EEK":"Estonian Kroon",
                                "ლ":"Georgian Lari",
                                "kr":"Icelandic Krona",
                                "Ft":"Hungarian Forint",
                                "лв":"Kazakhstani Tenge",
                                "Ls":"Latvian Lats",
                                "CHF":"Swiss Franc",
                                "Lt":"Lithuanian Litas",
                                "ден":"Macedonian Denar",
                                "₤":"Maltese Lira",
                                "L":"Moldovan Leu",
                                "kr":"Norwegian Krone",
                                "zł":"Polish Zloty",
                                "lei":"Romanian Leu",
                                "₽":"Russian Ruble",
                                "Дин.":"Serbian Dinar",
                                "Sk":"Slovak Koruna",
                                "kr":"Swedish Krona",
                                "CHF":"Swiss Franc",
                                "₺":"Turkish New Lira",
                                "₴":"Ukrainian Hryvnia",
                                "£":"Pound",
                                "BZ$":"Belize Dollar",
                                "₡":"Costa Rican Colon",
                                "RD$":"Dominican Peso",
                                "Q":"Guatemalan Quetzal",
                                "G":"Haitian Gourde",
                                "L":"Honduran Lempira",
                                "J$":"Jamaican Dollar",
                                "C$":"Nicaraguan Córdoba",
                                "B/.":"Panamanian Balboa",
                                "TT$":"Trinidad and Tobago Dollar",
                                "$b":"Bolivian Boliviano",
                                "Gs":"Paraguay Guarani",
                                "S/.":"Peruvian Nuevo Sol",
                                "$U":"Uruguayan peso",
                                "Bs":"Venezuelan Bolivar",
                                "K":"Papua New Guinea Kina",
                                "WS$":"Samoan Tala",
                                "T$":"Tongan Pa\'Anga",
                                "VT":"Vanuatu Vatu"}

abbreviated_currency_symbols_to_currency_name_dict = {'AFN': 'Afghanistani Afghani',
                                                         'AMD': 'Armenian Dram',
                                                         'AZN': 'Azerbaijani Manat',
                                                         'BHD': 'Bahraini Dinar',
                                                         'BDT': 'Bangladeshi Taka',
                                                         'BTN': 'Bhutanese Ngultrum',
                                                         'BND': 'Brunei Dollar',
                                                         'KHR': 'Cambodian Riel',
                                                         'CNY': 'Chinese Yuan Renminbi',
                                                         'CYP': 'Cypriot Pound',
                                                         'GEL': 'Georgian Lari',
                                                         'INR': 'Indian Rupee',
                                                         'IDR': 'Indonesian Rupiah',
                                                         'IRR': 'Iranian Rial',
                                                         'IQD': 'Iraqi Dinar',
                                                         'ILS': 'Israeli New Sheqel',
                                                         'JPY': 'Japanese Yen',
                                                         'JOD': 'Jordanian Dinar',
                                                         'KZT': 'Kazakhstani Tenge',
                                                         'KWD': 'Kuwaiti Dinar',
                                                         'KGS': 'Kyrgyzstani Som',
                                                         'LAK': 'Lao Kip',
                                                         'LBP': 'Lebanese Pound',
                                                         'MYR': 'Malaysian Ringgit',
                                                         'MVR': 'Maldives Rufiyaa',
                                                         'MNT': 'Mongolian Tugrik',
                                                         'MMK': '(Burma) Myanmar Kyat',
                                                         'NPR': 'Nepalese Rupee',
                                                         'KPW': 'North Korean Won',
                                                         'OMR': 'Omani Rial',
                                                         'PKR': 'Pakistan Rupee',
                                                         'PHP': 'Philippine Peso',
                                                         'QAR': 'Qatari Riyal',
                                                         'RUB': 'Russian Ruble',
                                                         'SAR': 'Saudi Arabian Riyal',
                                                         'SGD': 'Singapore Dollar',
                                                         'KRW': 'Korean Won',
                                                         'LKR': 'Sri Lankan Rupee',
                                                         'SYP': 'Syrian Pound',
                                                         'TWD': 'New Taiwan Dollar',
                                                         'TJS': 'Tajikistan Somoni',
                                                         'THB': 'Thai Baht',
                                                         'USD': 'United States Dollar',
                                                         'TRY': 'Turkish New Lira',
                                                         'TMM': 'Turkmenistani Manat',
                                                         'AED': 'United Arab Emirates Dirham',
                                                         'UZS': 'Uzbekistani Som',
                                                         'VND': 'Viet Nam Dong',
                                                         'YER': 'Yemeni Rial',
                                                         'DZD': 'Algerian Dinar',
                                                         'AOA': 'Angolan Kwanza',
                                                         'XOF': 'West African CFA',
                                                         'BWP': 'Botswana Pula',
                                                         'BIF': 'Burundian Franc',
                                                         'CVE': 'Cape Verde Escudo',
                                                         'XAF': 'Central African CFA',
                                                         'KMF': 'Comorian Franc',
                                                         'CDF': 'Congolese franc',
                                                         'DJF': 'Djiboutian Franc',
                                                         'EGP': 'Egyptian Pound',
                                                         'ERN': 'Eritrean Nakfa',
                                                         'ETB': 'Ethiopian Birr',
                                                         'GMD': 'Gambian Dalasi',
                                                         'GHC': 'Ghanaian Cedi',
                                                         'GNF': 'Guinean Franc',
                                                         'KES': 'Kenyan Shilling',
                                                         'LSL': 'Lesotho Loti',
                                                         'LRD': 'Liberian Dollar',
                                                         'LYD': 'Libyan Dinar',
                                                         'MGA': 'Malagasy Ariary',
                                                         'MWK': 'Malawian Kwacha',
                                                         'MRO': 'Mauritanian Ouguiya',
                                                         'MUR': 'Mauritian Rupee',
                                                         'MAD': 'Moroccan Dirham',
                                                         'MZN': 'Mozambican Metical',
                                                         'NAD': 'Namibian Dollar',
                                                         'NGN': 'Nigerian Naira',
                                                         'RWF': 'Rwandan Franc',
                                                         'STD': 'Sao Tome Dobra',
                                                         'SCR': 'Seychelles Rupee',
                                                         'SLL': 'Sierra Leonean Leone',
                                                         'SOS': 'Somali Shilling',
                                                         'ZAR': 'South African Rand',
                                                         'SSP': 'South Sudanese pound',
                                                         'SDG': 'Sudanese pound',
                                                         'SZL': 'Swazi Lilangeni',
                                                         'TZS': 'Tanzanian Shilling',
                                                         'TND': 'Tunisian Dinar',
                                                         'UGX': 'Ugandan Shilling',
                                                         'ZMK': 'Zambian Kwacha',
                                                         'ZWD': 'Zimbabwean Dollar',
                                                         'ALL': 'Albanian Lek',
                                                         'EUR': 'European Euro',
                                                         'BYR': 'Belarusian Ruble',
                                                         'BAM': 'Bosnia-Herzegovina Convertible Mark',
                                                         'BGN': 'Bulgarian Lev',
                                                         'HRK': 'Croatian Kuna',
                                                         'CZK': 'Czech Koruna',
                                                         'DKK': 'Danish Krone',
                                                         'EEK': 'Estonian Kroon',
                                                         'HUF': 'Hungarian Forint',
                                                         'ISK': 'Icelandic Krona',
                                                         'LVL': 'Latvian Lats',
                                                         'CHF': 'Swiss Franc',
                                                         'LTL': 'Lithuanian Litas',
                                                         'MKD': 'Macedonian Denar',
                                                         'MTL': 'Maltese Lira',
                                                         'MDL': 'Moldovan Leu',
                                                         'NOK': 'Norwegian Krone',
                                                         'PLN': 'Polish Zloty',
                                                         'RON': 'Romanian Leu',
                                                         'RSD': 'Serbian Dinar',
                                                         'SKK': 'Slovak Koruna',
                                                         'SEK': 'Swedish Krona',
                                                         'UAH': 'Ukrainian Hryvnia',
                                                         'GBP': 'United Kingdom Pound Sterling',
                                                         'XCD': 'East Caribbean Dollar',
                                                         'BSD': 'Bahamian Dollar',
                                                         'BBD': 'Barbados Dollar',
                                                         'BZD': 'Belize Dollar',
                                                         'CAD': 'Canadian Dollar',
                                                         'CRC': 'Costa Rican Colon',
                                                         'CUC': 'Cuban Convertible Peso',
                                                         'DOP': 'Dominican Peso',
                                                         'GTQ': 'Guatemalan Quetzal',
                                                         'HTG': 'Haitian Gourde',
                                                         'HNL': 'Honduran Lempira',
                                                         'JMD': 'Jamaican Dollar',
                                                         'MXN': 'Mexican Peso',
                                                         'NIO': 'Nicaraguan Córdoba',
                                                         'PAB': 'Panamanian Balboa',
                                                         'TTD': 'Trinidad and Tobago Dollar',
                                                         'ARS': 'Argentine Peso',
                                                         'BOB': 'Bolivian Boliviano',
                                                         'BRL': 'Brazilian Real',
                                                         'CLP': 'Chilean Peso',
                                                         'COP': 'Colombian Peso',
                                                         'GYD': 'Guyanese Dollar',
                                                         'PYG': 'Paraguay Guarani',
                                                         'PEN': 'Peruvian Nuevo Sol',
                                                         'SRD': 'Suriname Dollar',
                                                         'UYU': 'Uruguayan peso',
                                                         'VEF': 'Venezuelan Bolivar',
                                                         'AUD': 'Australian Dollar',
                                                         'FJD': 'Fiji Dollar',
                                                         'NZD': 'New Zealand Dollar',
                                                         'PGK': 'Papua New Guinea Kina',
                                                         'WST': 'Samoan Tala',
                                                         'SBD': 'Solomon Islands Dollar',
                                                         'TOP': 'Tongan Pa\'Anga',
                                                         'VUV': 'Vanuatu Vatu'}