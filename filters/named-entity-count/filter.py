import operator
from typing import List

import spacy

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import (
    SentenceAndTargetOperation,
    SentenceOperation,
)
from tasks.TaskTypes import TaskType


class NamedEntityCountFilter(SentenceOperation):
    """
    A filter on the count of named entities in a sentence, with different arithmetic operators.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["named-entity", "count"]

    def __init__(self, op: str = ">=", threshold: int = 1):
        super().__init__()
        self.operator = self.parse_operator(op)
        self.threshold = threshold
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    @staticmethod
    def parse_operator(op):
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "==": operator.eq,
        }
        return ops[op]

    def filter(self, sentence: str = None) -> bool:
        tokenized = self.nlp(sentence, disable=["parser", "tagger"])
        named_entities = tokenized.ents
        return self.operator(len(named_entities), self.threshold)


class SentenceAndTargetNamedEntityCountFilter(SentenceAndTargetOperation):
    """
    An Example filter for SentenceAndTargetNamedEntityCountFilter interface.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    src_locales = ["en"]
    tgt_languages = ["en"]

    def __init__(self, ops: List[str] = None, thresholds: List[int] = None):
        super().__init__()
        self.operators = [
            NamedEntityCountFilter.parse_operator(op) for op in ops
        ]
        self.thresholds = thresholds
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

        self._sanity_check()

    def _sanity_check(self):
        assert (
            len(self.operators) == 2
        ), "SentenceAndTargetOperation only support two inputs."
        assert (
            len(self.thresholds) == 2
        ), "SentenceAndTargetOperation only support two inputs."

    def filter(self, sentence: str = None, target: str = None) -> bool:
        tokenized_sentence = self.nlp(sentence, disable=["parser", "tagger"])
        tokenized_target = self.nlp(target, disable=["parser", "tagger"])

        named_entities_sentence = tokenized_sentence.ents
        named_entities_target = tokenized_target.ents

        condition1 = self.operators[0](
            len(named_entities_sentence), self.thresholds[0]
        )
        condition2 = self.operators[1](
            len(named_entities_target), self.thresholds[1]
        )
        return condition1 and condition2
