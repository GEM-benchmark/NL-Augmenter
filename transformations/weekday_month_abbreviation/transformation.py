import json
import os
import re
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def weekday_month_abbreviate(text, abbreviations, expansions, max_outputs=1):

    regex = re.compile(
        "(%s)"
        % (
            "|".join([x + "(?!s)" for x in abbreviations.keys()])
            + "|"
            + "|".join([x.replace(".", "\\.") for x in expansions.keys()])
        )
    )

    return [
        regex.sub(
            lambda y: {**abbreviations, **expansions}[
                y.string[y.start() : y.end()]
            ],
            text,
        )
    ]


class WeekdayMonthAbbreviation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(self):
        super().__init__()

        abbreviations_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "weekday_month_abb_en.json",
        )
        expansions_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "weekday_month_exp_en.json",
        )

        self.abbreviations = json.load(open(abbreviations_path, "r"))
        self.expansions = json.load(open(expansions_path, "r"))

    def generate(self, sentence: str) -> List[str]:
        perturbed_texts = weekday_month_abbreviate(
            text=sentence,
            abbreviations=self.abbreviations,
            expansions=self.expansions,
        )
        return perturbed_texts
