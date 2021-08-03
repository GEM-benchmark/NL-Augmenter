from transformations.replace_financial_amounts.entity_financial_amount import (
    CURRENCIES_WITH_EXCHANGE_RATE,
    get_amount_and_currency,
    generate_new_amount,
    convert_currency,
    change_currency,
    generate_financial_amount_for_currency_with_exchange_rate,
    generate_financial_amount_for_specific_currency,
    format_amount,
)
import pytest

amount_and_currencies = [
    ("$ 300 000", 300000.00, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    ("300 000 $", 300000.00, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    ("US dollars 2.15", 2.15, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    ("1,100.00 US dollars", 1100.00, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    ("£ 1200 . 10", 1200.10, CURRENCIES_WITH_EXCHANGE_RATE["pound"]),
    ("€ 300 , 000 . 10", 300000.10, CURRENCIES_WITH_EXCHANGE_RATE["euro"]),
    ("35000 euros", 35000.00, CURRENCIES_WITH_EXCHANGE_RATE["euro"]),
    ("€ 300 , 000 . 10", 300000.10, CURRENCIES_WITH_EXCHANGE_RATE["euro"]),
    ("2000 CAD", 2000.00, {"symbol": ["CAD"], "rate": 1.0}),
    ("$ 12 USD", 12, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    ("USD $12", 12, CURRENCIES_WITH_EXCHANGE_RATE["dollar"]),
    (" 2 447.47 JPY ", 2447.47, CURRENCIES_WITH_EXCHANGE_RATE["yen"]),
]


@pytest.mark.parametrize(
    "sample,expected_amount,expected_currency", amount_and_currencies
)
def test_get_amount_and_currency(sample, expected_amount, expected_currency):
    amount, currency = get_amount_and_currency(sample)

    assert amount == expected_amount
    assert currency == expected_currency


def test_generate_new_amount():
    amount = 1000
    percentage_financial_amount_variation = 10
    new_amount = generate_new_amount(
        amount, percentage_financial_amount_variation
    )
    assert new_amount == 1100


def test_convert_currency():
    amount = 1000
    old_rate = CURRENCIES_WITH_EXCHANGE_RATE["dollar"]["rate"]
    new_rate = CURRENCIES_WITH_EXCHANGE_RATE["euro"]["rate"]

    new_amount = convert_currency(amount, old_rate, new_rate)
    assert new_amount == 840.34


def test_change_currency_normal_case():
    amount = 1000
    currency = CURRENCIES_WITH_EXCHANGE_RATE["dollar"]
    currencies_generated = ["pound", "yen", "yuan", "bitcoin"]

    new_amount, new_currency = change_currency(
        amount, currency, currencies_generated
    )

    assert new_amount == 840.34
    assert new_currency == CURRENCIES_WITH_EXCHANGE_RATE["euro"]


def test_change_currency_corner_case():
    amount = 1000
    currency = CURRENCIES_WITH_EXCHANGE_RATE["dollar"]
    currencies_generated = ["pound", "yen", "yuan", "bitcoin", "euro"]

    new_amount, new_currency = change_currency(
        amount, currency, currencies_generated
    )

    assert new_amount == 1000
    assert new_currency == CURRENCIES_WITH_EXCHANGE_RATE["dollar"]


def test_generate_financial_amount():
    amount = 1000
    currency = CURRENCIES_WITH_EXCHANGE_RATE["dollar"]
    percentage_financial_amount_variation = 10

    (
        n_format,
        n_currency,
        n_symbol,
    ) = generate_financial_amount_for_currency_with_exchange_rate(
        amount, currency, [], percentage_financial_amount_variation
    )

    new_amount, new_currency_found = get_amount_and_currency(n_format)

    assert new_amount != amount
    assert n_currency == new_currency_found
    assert n_symbol in new_currency_found["symbol"]
    assert n_symbol in n_format


def test_generate_specific_financial_amount():
    amount = 1000
    currency = CURRENCIES_WITH_EXCHANGE_RATE["dollar"]
    currency_to_generate = CURRENCIES_WITH_EXCHANGE_RATE["euro"]
    symbol_to_use = "EUR"
    percentage_financial_amount_variation = -10

    for _ in range(1000):
        generated_amount = generate_financial_amount_for_specific_currency(
            amount,
            currency,
            currency_to_generate,
            symbol_to_use,
            percentage_financial_amount_variation,
        )

        assert generated_amount in ["756.30 EUR", "756 EUR"]


amount_tested = [
    (300.00, ["300", "300.00"]),
    (300.32, ["300.32", "300", "300.00"]),
    (
        30000.00,
        [
            "30k",
            "30 k",
            "30K",
            "30 K",
            "30 000",
            "30000.00",
            "30,000.00",
            "30000",
        ],
    ),
    (
        2132.12,
        [
            "2 132.12",
            "2132.12",
            "2,132.12",
            "2132",
            "2 132.00",
            "2,132",
            "2 132",
            "2,132.00",
            "2132.00",
        ],
    ),
    (200000000.00, ["200000000"]),
]


@pytest.mark.parametrize("amount,expected", amount_tested)
def test_format_amount(amount, expected):
    new_amount = format_amount(amount)
    assert new_amount in expected
