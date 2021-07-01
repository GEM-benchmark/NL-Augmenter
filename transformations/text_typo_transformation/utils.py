import re
import regex
from typing import List, Optional, Tuple
from nlpaug import Augmenter  # @manual
from nlpaug.util import Method  # @manual

PARENS_BRACKETS = [
    (re.compile(r"\s([\[\(\{\<])\s"), r" \1"),
    (re.compile(r"\s([\]\)\}\>])\s"), r"\1 "),
]

PUNCTUATION = [
    (re.compile(r"\s([-])\s"), r"\1"),  # Zero pad
    (re.compile(r"(\s)?([#])\s"), r"\2"),  # Hashtags
    (re.compile(r"\s([,;:%])\s"), r"\1 "),  # Right pad
    (re.compile(r"([\$])\s([\d])"), r"\1\2"),  # $ amounts
    (re.compile(r"([\$])\s"), r"\1"),  # Consecutive $ signs
    (re.compile(r"(\s)?([\.\?\!])"), r"\2"),  # End punctuation
]

QUOTES = [
    (re.compile(r"([\'])\s(.*?)\s([\'])"), r"\1\2\3"),
    (re.compile(r"([\"])\s(.*?)\s([\"])"), r"\1\2\3"),
    (re.compile(r"\s(\')\s"), r"\1 "),
]

TOKENIZER_REGEXPS = (
    r"""
    (?: [\w]+['][\w]+)             # Contractions
    |
    (?:[+\-]?\d+[,/.:^]\d+)        # Numbers (fractions, decimals, time, ratios)
    |
    (?:[\w_]+)                     # Words without punctuation
    |
    (?:\S)                         # Everything else
    """,
)

TOKENIZER_REGEX = regex.compile(
    r"""(%s)""" % "|".join(TOKENIZER_REGEXPS), regex.VERBOSE | regex.UNICODE
)


def tokenize(text: str) -> List[str]:
    return TOKENIZER_REGEX.findall(text)


def detokenize(tokens: List[str]) -> str:
    text = " ".join(tokens)
    text = " " + text + " "

    for regexp, substitution in PARENS_BRACKETS:
        text = regexp.sub(substitution, text)

    for regexp, substitution in PUNCTUATION:
        text = regexp.sub(substitution, text)

    for regexp, substitution in QUOTES:
        text = regexp.sub(substitution, text)

    return text.strip()


def validate_augmenter_params(
    aug_char_min: int,
    aug_char_max: int,
    aug_char_p: float,
    aug_word_min: int,
    aug_word_max: int,
    aug_word_p: float,
) -> None:
    assert aug_char_min >= 0, "aug_char_min must be non-negative"
    assert aug_char_max >= 0, "aug_char_max must be non-negative"
    assert 0 <= aug_char_p <= 1, "aug_char_p must be a value in the range [0, 1]"
    assert aug_word_min >= 0, "aug_word_min must be non-negative"
    assert aug_word_max >= 0, "aug_word_max must be non-negative"
    assert 0 <= aug_word_p <= 1, "aug_word_p must be a value in the range [0,1]"


def get_aug_idxes(
    augmenter: Augmenter,
    tokens: List[str],
    filtered_idxes: List[int],
    aug_cnt: int,
    mode: str,
    min_char: Optional[int] = None,
) -> List[int]:
    assert (
        mode in Method.getall()
    ), "Expected 'mode' to be a value defined in nlpaug.util.method.Method"

    priority_idxes = []
    priority_words = getattr(augmenter, "priority_words", None)

    if mode == Method.WORD and priority_words is not None:
        for i, token in enumerate(tokens):
            if token in priority_words:
                if min_char is None or len(token) >= min_char:
                    priority_idxes.append(i)

    idxes = []
    for i in filtered_idxes:
        if i not in priority_idxes:
            if min_char is None or len(tokens[i]) >= min_char:
                idxes.append(i)

    if len(priority_idxes) + len(idxes) == 0:
        return []

    if len(priority_idxes) <= aug_cnt:
        aug_idxes = priority_idxes
        aug_cnt -= len(priority_idxes)
        if len(idxes) < aug_cnt:
            aug_cnt = len(idxes)
        aug_idxes += augmenter.sample(idxes, aug_cnt)
    else:
        aug_idxes = augmenter.sample(priority_idxes, aug_cnt)

    return aug_idxes
