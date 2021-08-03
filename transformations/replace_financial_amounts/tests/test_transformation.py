from transformations.replace_financial_amounts.transformation import (
    create_tokens,
    indexes_of_financial_amount,
    tag_tokens,
    replace,
    is_numeric,
    merge,
    is_numeric_token,
)
import pytest


@pytest.mark.parametrize(
    "text_input, expected",
    [
        ("39", True),
        ("Could", False),
    ],
    ids=["numeric value", "non-numeric value"],
)
def test_is_numeric(text_input, expected):
    actual = is_numeric(text_input)
    assert actual is expected


def test_create_tokens():
    res = create_tokens("Could you buy me giftcard at 39.99€")
    assert res[6]["category"] == "numeric"
    assert not res[6]["is_financial_amount"]


@pytest.mark.parametrize(
    "text_input, len_input_tokens, index_financial_amount, len_after_tag",
    [
        ("Could you buy me giftcard at 39.99€", 8, 6, 7),
        ("I owe Fred $20", 5, 3, 4),
    ],
    ids=["simple", "dollar example"],
)
def test_tag_tokens(
    text_input, len_input_tokens, index_financial_amount, len_after_tag
):
    tokens = create_tokens(text_input)
    # test nb token  before tagging
    assert len(tokens) == len_input_tokens
    tagged_token = tag_tokens(tokens)

    for i, token in enumerate(tagged_token):
        if i != index_financial_amount:
            assert not token["is_financial_amount"]
        else:
            assert token["is_financial_amount"]
    # test that some token have been merged
    assert len(tagged_token) == len_after_tag


@pytest.mark.parametrize(
    "token, expected",
    [
        (
            {
                "text": "39.99€",
                "is_financial_amount": True,
                "category": "other",
            },
            "50 000 XOF",
        ),
        (
            {
                "text": "USD 20 ",
                "is_financial_amount": True,
                "category": "other",
            },
            "15.5€ ",
        ),
    ],
    ids=[
        "without space",
        "with space",
    ],
)
def test_replace(token, expected):
    replace(token, expected)
    assert token["text"] == expected


def test_indexes_of_financial_amount():
    tokens = create_tokens("Could you buy me giftcard at 39.99 €")
    start, end = indexes_of_financial_amount(6, tokens)
    assert start == 6
    assert end == 6


test_tokens = [
    {
        "text": "I ",
        "category": "other",
        "is_financial_amount": False,
    },
    {
        "text": "owe ",
        "category": "other",
        "is_financial_amount": False,
    },
    {
        "text": "Fred ",
        "category": "other",
        "is_financial_amount": False,
    },
    {
        "text": "$",
        "category": "other",
        "is_financial_amount": False,
    },
    {
        "text": "20",
        "category": "numeric",
        "is_financial_amount": False,
    },
]


@pytest.mark.parametrize(
    "tokens, len_tokens, start, end, len_merged_tokens",
    [
        (test_tokens, 5, 3, 4, 4),
        (test_tokens, 5, 3, 3, 5),
    ],
    ids=[
        "different index",
        "same index",
    ],
)
def test_merge(tokens, len_tokens, start, end, len_merged_tokens):
    assert len(tokens) == len_tokens
    new_tokens = merge(start, end, tokens)
    assert len(new_tokens) == len_merged_tokens


@pytest.mark.parametrize(
    "token, expected",
    [
        (
            {
                "text": "I ",
                "category": "other",
                "is_financial_amount": False,
            },
            False,
        ),
        (
            {
                "text": "30 ",
                "category": "numeric",
                "is_financial_amount": False,
            },
            False,
        ),
        (
            {
                "text": "299",
                "category": "numeric",
                "is_financial_amount": False,
            },
            True,
        ),
    ],
    ids=[
        "non-numeric",
        "numeric - bad shape",
        "numeric",
    ],
)
def test_is_numeric_token(token, expected):
    actual = is_numeric_token(token, expected_length=3)
    assert actual is expected
