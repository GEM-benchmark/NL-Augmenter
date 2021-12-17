import json
import re

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

"""A filter selecting for British spellings and slang.

Attributes
----------
britwords_required : int
    the number of British words required for a passage to pass the filter
"""


class EnglishnessFilter(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["lexical", "rule-based"]

    def __init__(self, britwords_required=1):
        super().__init__()
        self.britwords_required = britwords_required

    def filter(self, sentence: str = None) -> bool:
        britwords = get_britwords()

        num_britwords = 0
        for bword in britwords:
            num_britwords += len(
                re.findall("(?<![a-zA-Z])" + bword + "(?![a-zA-Z])", sentence)
            )
            num_britwords += len(
                re.findall(
                    "(?<![a-zA-Z])"
                    + bword[0].upper()
                    + bword[1:]
                    + "(?![a-zA-Z])",
                    sentence,
                )
            )

        return num_britwords >= self.britwords_required


def get_britwords():
    britwords = []

    spelling_json_file = open("filters/englishness/spelling_map.json")
    spelling_map = json.load(spelling_json_file)
    britwords += spelling_map.values()

    vocab_json_file = open("filters/englishness/vocab_map.json")
    vocab_map = json.load(vocab_json_file)
    britwords += vocab_map.values()

    britslang = [
        "tosser",
        "blimey",
        "wanker",
        "chuffed",
        "sod off",
        "wonky",
        "whinge",
        "tenner",
        "fiver",
        "quid",
        "toff",
        "skive",
        "scouse",
        "scouser",
        "cockney",
        "nicked",
        "nutter",
        "gobsmacked",
        "chap",
        "bugger",
        "anticlockwise",
        "anti-clockwise",
        "nosh",
        "bollocks",
        "ponce",
        "bangers",
        "telly",
        "knickers",
        "uni",
        "albion",
        "chunder",
        "fortnight",
        "grockel",
        "kerfuffle",
        "scrummy",
    ]

    britwords += britslang

    return set(britwords)
