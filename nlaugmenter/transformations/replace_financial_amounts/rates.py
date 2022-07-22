import sys

from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates, RatesNotAvailableError

# Those default exchange rates below are those used against 1 USD as of August 2021.
EXCHANGE_RATES = {
    "EUR_to_USD": 1.19,
    "GBP_to_USD": 1.39,
    "JPY_to_USD": 0.0092,
    "CNY_to_USD": 0.15,
    "BTC_to_USD": 37716,
}

if not any([mod in sys.modules for mod in ["unittest", "test", "pytest"]]):
    c = CurrencyRates()
    b = BtcConverter()
    try:
        EXCHANGE_RATES = {
            "EUR_to_USD": c.get_rate("EUR", "USD"),
            "GBP_to_USD": c.get_rate("GBP", "USD"),
            "JPY_to_USD": c.get_rate("JPY", "USD"),
            "CNY_to_USD": c.get_rate("CNY", "USD"),
            "BTC_to_USD": b.get_latest_price("USD"),
        }
    except RatesNotAvailableError:
        print(
            "Warning: problem loading actual conversion rates. Switching to default rates."
        )


CURRENCIES_WITH_EXCHANGE_RATE = {
    "dollar": {
        "name": "dollar",
        "symbol": ["$", "dollar", "dollars", "USD", "US dollars", "Dollars"],
        "rate": 1.0,
    },
    "euro": {
        "name": "euro",
        "symbol": ["€", "euro", "euros", "EUR", "Euros"],
        "rate": EXCHANGE_RATES["EUR_to_USD"],
    },
    "pound": {
        "name": "pound",
        "symbol": ["£", "pound", "pounds", "GBP", "Pounds"],
        "rate": EXCHANGE_RATES["GBP_to_USD"],
    },
    "yen": {
        "name": "yen",
        "symbol": ["¥", "yen", "JPY", "Yen"],
        "rate": EXCHANGE_RATES["JPY_to_USD"],
    },
    "yuan": {
        "name": "yuan",
        "symbol": ["yuan", "CNY", "RMB"],
        "rate": EXCHANGE_RATES["CNY_to_USD"],
    },
    "bitcoin": {
        "name": "bitcoin",
        "symbol": ["฿", "bitcoin", "bitcoins", "BTC"],
        "rate": EXCHANGE_RATES["BTC_to_USD"],
    },
}
