import pytest
import copy
from transformations.replace_abbreviation_and_acronyms.transformation import (
    load,
    separate_into_contracted_and_expanded_form,
    indexes_of_abbreviations,
    merge,
    create_tokens,
    ReplaceAbbreviations,
)


tokens_contracted_end = [
    {
        "text": "I",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "am",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "leaving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "asap",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]

tokens_expanded_end = [
    {
        "text": "I",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "am",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "leaving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "soon",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "possible",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]

tokens_expanded_middle = [
    {
        "text": "I",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "am",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "leaving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "soon",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "possible",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "thanks",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]
tokens_contracted_middle = [
    {
        "text": "I",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "am",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "leaving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "asap",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "bye",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]


def test_load():
    abb = load("abbreviations.txt")
    assert len(abb) == 130


def test_separate_into_contracted_and_expanded_form():
    input = [
        ["ACCT", "Account"],
        ["AIDA", "Attention, interest, desire, action"],
        ["AP", "Accounts payable"],
    ]
    contracted, expanded = separate_into_contracted_and_expanded_form(input)
    assert len(expanded) == len(input)
    assert len(contracted) == len(input)


tokens_expanded = [
    {
        "text": "I",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "am",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "moving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "soon",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "as",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "possible",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]
tokens_double_contracted = [
    {
        "text": "The",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "CTO",
        "is_a_verb": False,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "is",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "leaving",
        "is_a_verb": True,
        "end_space": " ",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
    {
        "text": "asap",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": False,
        "is_expanded_abbreviation": False,
    },
]


@pytest.mark.parametrize(
    "sentence, indexes_of_abbreviations, length",
    [
        ("I am leaving asap", [3], 4),
        ("I am moving as soon as possible", [3], 4),
        ("The CTO is leaving asap", [1, 4], 5),
        (
            "The new Research and development department was assigned a chief technology officer today",
            [2, 7],
            9,
        ),
    ],
    ids=[
        "contracted abbr",
        "expanded abbr",
        "double contracted abbr",
        "double expanded abbr",
    ],
)
def test_tag_tokens(sentence, indexes_of_abbreviations, length):
    replacer = ReplaceAbbreviations()
    tokens = create_tokens(sentence)
    res = replacer.tag_tokens(tokens)
    for idx in indexes_of_abbreviations:
        assert res[idx]["is_abbreviation"]
    assert len(res) == length


@pytest.mark.parametrize(
    "tokens, start, finish, expected_length, expected_is_expanded",
    [
        (copy.deepcopy(tokens_contracted_end), 3, 3, 4, False),
        (tokens_expanded, 3, 6, 4, True),
    ],
    ids=[
        "contracted abbr",
        "expanded abbr",
    ],
)
def test_merge(tokens, start, finish, expected_length, expected_is_expanded):
    res = merge(tokens, start, finish)
    assert res[start]["is_abbreviation"]
    assert len(res) == expected_length
    assert res[start]["is_expanded_abbreviation"] == expected_is_expanded


@pytest.mark.parametrize(
    "sentence, abbreviation, expected_start, expected_finish",
    [
        ("I am leaving as soon as possible", "as soon as possible", 3, 6),
        ("I am leaving asap", "asap", 3, 3),
        (
            "I am leaving as soon as possible thanks",
            "as soon as possible",
            3,
            6,
        ),
        ("I am leaving asap", "asap", 3, 3),
        (
            "The new Research and development department was assigned a chief technology officer today.",
            "chief analytics officer",
            -1,
            -1,
        ),
        ("Kapur's credit,", "credit", 2, 2),
    ],
    ids=[
        "contracted abbr - end of sentence",
        "expanded abbr - end of sentence",
        "expanded abbr - middle of sentence",
        "contracted abbr - middle of sentence",
        "multiple expanded - not found",
        "single word expanded",
    ],
)
def test_indexes_of_abbreviations(
    sentence, abbreviation, expected_start, expected_finish
):
    tokens = create_tokens(sentence)
    start, finish = indexes_of_abbreviations(tokens, abbreviation)
    assert start == expected_start
    assert finish == expected_finish


def test_replace_abbreviation():
    token = {
        "text": "asap",
        "is_a_verb": False,
        "end_space": "",
        "is_abbreviation": True,
        "is_expanded_abbreviation": False,
    }
    replacer = ReplaceAbbreviations()
    replacer.replace_abbreviation(token)
    assert token["text"] == "as soon as possible"
