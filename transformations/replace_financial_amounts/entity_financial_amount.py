from typing import List, Dict, Tuple
import random
import re
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)


def load_currency_abbreviation_file(path: str) -> List[str]:
    """
    Return a list of currency abbreviations present as one value per line in a file.
    """
    with open(
        os.path.join(__location__, path), "r", encoding="utf-8"
    ) as _file:
        file_content = _file.read()
        result = file_content.split("\n")

    if result[-1] == "":
        return result[:-1]

    return result


WORLD_CURRENCY_ABBREVIATIONS = load_currency_abbreviation_file(
    "currency_abbr.txt"
)

# The exchange rate used bellow are those used against 1 USD as of August 2021.
CURRENCIES_WITH_EXCHANGE_RATE = {
    "dollar": {
        "name": "dollar",
        "symbol": ["$", "dollar", "dollars", "USD", "US dollars", "Dollars"],
        "rate": 1.0,
    },
    "euro": {
        "name": "euro",
        "symbol": ["€", "euro", "euros", "EUR", "Euros"],
        "rate": 1.19,
    },
    "pound": {
        "name": "pound",
        "symbol": ["£", "pound", "pounds", "GBP", "Pounds"],
        "rate": 1.39,
    },
    "yen": {
        "name": "yen",
        "symbol": ["¥", "yen", "JPY", "Yen"],
        "rate": 0.0092,
    },
    "yuan": {"name": "yuan", "symbol": ["yuan", "CNY", "RMB"], "rate": 0.15},
    "bitcoin": {
        "name": "bitcoin",
        "symbol": ["฿", "bitcoin", "bitcoins", "BTC"],
        "rate": 37716,
    },
}

CURRENCIES_WITH_EXCHANGE_RATE_SYMBOLS = []
for _currency in CURRENCIES_WITH_EXCHANGE_RATE:
    CURRENCIES_WITH_EXCHANGE_RATE_SYMBOLS += CURRENCIES_WITH_EXCHANGE_RATE[
        _currency
    ]["symbol"]
CURRENCY_SYMBOLS = ["$", "£", "₤", "¥", "฿", "€"]


def generate_new_amount(
    amount: float, percentage_financial_amount_variation: int
) -> float:
    """
    | Generate new amount from current amount.
    |  The value of percentage_financial_amount_variation should be between 1 and 20 to ensure coherence.
    """
    percentage_value = amount * (percentage_financial_amount_variation / 100)
    return round(amount + percentage_value, 2)


def generate_new_symbol(symbol: List[str]) -> str:
    """
    Select a new currency symbol.
    """
    index = random.randint(0, len(symbol) - 1)
    return symbol[index]


def generate_new_format(amount: float, symbol: str) -> str:
    """
    Format the numerical amount and place the currency symbol appropriately.
    """
    if symbol in CURRENCY_SYMBOLS:
        formatted_amount = format_amount(amount)
        return f"{symbol} {formatted_amount}"

    formatted_amount = format_amount(amount)
    return f"{formatted_amount} {symbol}"


def convert_currency(amount: float, old_rate: float, new_rate: float) -> float:
    """
    Convert the amount of a currency to another amount of a currency based on a conversion rate.
    """
    return round(amount * old_rate / new_rate, 2)


def change_currency(
    amount: float, currency: Dict, currencies_generated: List[str]
) -> Tuple[float, Dict]:
    """
    | Change a currency to another currency.
    | The currency generated is necessarily different for the current one and from those generated previously.
    """
    all_keys = list(CURRENCIES_WITH_EXCHANGE_RATE.keys())

    # As we want to generate a new currency, we remove the current currency
    all_keys.remove(currency["name"])

    # We must delete the currencies already generated to keep a context
    for currency_generated in currencies_generated:
        if currency_generated in all_keys:
            all_keys.remove(currency_generated)

    # We keep the same currency if there is no other choice.
    if all_keys:
        new_key = random.choice(all_keys)
    else:
        new_key = currency["name"]

    # Convert the amount to the new currency using the appropriate conversion rate.
    new_currency = CURRENCIES_WITH_EXCHANGE_RATE[new_key]
    new_amount = convert_currency(
        amount, currency["rate"], new_currency["rate"]
    )

    return new_amount, new_currency


def generate_financial_amount_for_currency_with_exchange_rate(
    amount: float,
    currency: Dict,
    currencies_generated: List[str],
    percentage_financial_amount_variation: int,
) -> Tuple[str, Dict, str]:
    """
    Generate a new financial amount, potentially changing the currency as well.
    """
    new_amount = generate_new_amount(
        amount, percentage_financial_amount_variation
    )

    if currency["name"] in currencies_generated or random.choice(
        [True, False]
    ):
        new_amount, new_currency = change_currency(
            new_amount, currency, currencies_generated
        )
        new_symbol = generate_new_symbol(new_currency["symbol"])
    else:
        new_currency = currency
        new_symbol = generate_new_symbol(currency["symbol"])

    return (
        generate_new_format(new_amount, new_symbol),
        new_currency,
        new_symbol,
    )


def generate_financial_amount_for_specific_currency(
    amount: float,
    currency: Dict,
    currency_to_generate: Dict,
    encountered_symbol: str,
    percentage_financial_amount_variation: int,
) -> str:
    """
    Generate a new financial amount for a specific currency.
    """
    new_amount = generate_new_amount(
        amount, percentage_financial_amount_variation
    )
    new_amount = convert_currency(
        new_amount, currency["rate"], currency_to_generate["rate"]
    )

    return generate_new_format(new_amount, encountered_symbol)


def get_amount_and_currency(token_value: str) -> Tuple[float, Dict]:
    """
    Return the amount and the currency used in a string value.
    e.g.: `10,30 euros` -> `(10.30, CURRENCIES_WITH_EXCHANGE_RATE['euro'])`.
    """
    amount = re.findall(
        r"[0-9]+(?:\s?(?:,?\s?[0-9]{3})\s?)*\s?(?:\.?\s?[0-9]{2}|[kK]?)",
        token_value,
    )
    currency = [
        elt.strip()
        for elt in filter(None, token_value.split(" ".join(amount)))
        if elt.strip() != ""
    ]
    currency = determine_currency(currency)
    amount = determine_amount(amount)
    return amount, currency


def determine_currency(token_list: List[str]) -> Dict or None:
    """
    Return a currency, either as one from CURRENCIES_WITH_EXCHANGE_RATE or as a simple dictionary.
    """
    if len(token_list) == 1:
        currency = token_list[0]
        is_present_in_currencies = False

        for _, value in CURRENCIES_WITH_EXCHANGE_RATE.items():
            if currency in value["symbol"]:
                currency = value
                is_present_in_currencies = True
            if is_present_in_currencies:
                return currency

        if "US" in currency:
            return CURRENCIES_WITH_EXCHANGE_RATE["dollar"]

        return {"symbol": token_list, "rate": 1.0}

    if "US" in " ".join(token_list):
        return CURRENCIES_WITH_EXCHANGE_RATE["dollar"]

    return None


def determine_amount(token_list: List[str]) -> float:
    """
    Determine the amount as a float associated to the token_list.
    """
    amount = ""
    for token in token_list:
        amount += "".join(token.split())
    amount = amount.lower().replace("k", "000")
    amount = float(amount.replace(",", ""))

    return amount


def format_amount(amount: float) -> str:
    """
    | Formats randomly an amount as a string to be printed.
    | Formatted amounts are limited to a maximum of two decimal digits.
    """
    thousands = int(amount / 1000)
    hundreds = int(amount % 1000)
    decimal_str = re.sub(r".*\.", "", str("%.2f" % amount))[:2]

    # Amount is a multiple of 1000 (e.g.: 130 000)
    if 1000000 > amount > 1000 and hundreds == 0 and decimal_str == "00":
        potential_strings = ["k", " k", "K", " K", "000", " 000"]
        return f"{thousands}{random.choice(potential_strings)}"

    # Amount is over 1k but hundreds is != 0 (e.g.: 1 340)
    if 1000000 > amount > 1000 and decimal_str == "00":
        return f"{thousands}{random.choice(['', ' ', ','])}{'{:03d}'.format(hundreds)}"

    # Amount is over 1k (e.g.: 13 289,25)
    if 1000000 > amount > 1000:
        return f"{thousands}{random.choice(['', ' ', ','])}{'{:03d}'.format(hundreds)}{random.choice(['', '.' + decimal_str])}"

    # Amount is less than 1k (e.g. 34,59)
    if 1 < amount < 1000:
        return f"{hundreds}{random.choice(['', '.' + decimal_str])}"

    return f"{int(amount)}"
