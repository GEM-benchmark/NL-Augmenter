import operator
import spacy

from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from tasks.TaskTypes import TaskType
from typing import List

"""
A filter on text length (number of tokens).
"""


class TextLengthFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self, op: str = None, threshold: int = None):
        super().__init__()
        self.operator = self.parse_operator(op)
        self.threshold = threshold
        self.nlp = spacy.load("en_core_web_sm")

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
        tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        return self.operator(len(tokenized), self.threshold)


"""
An Example filter for SentenceAndTargetOperation interface.
"""


class SentenceAndTargetLengthFilter(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    src_locales = ["en"]
    tgt_locales = ["en"]

    def __init__(self, ops: List[str] = None, thresholds: List[int] = None):
        super().__init__()
        self.operators = [TextLengthFilter.parse_operator(op) for op in ops]
        self.thresholds = thresholds
        self.nlp = spacy.load("en_core_web_sm")

        self._sanity_check()

    def _sanity_check(self):
        assert (
            len(self.operators) == 2
        ), "SentenceAndTargetOperation only support two inputs."
        assert (
            len(self.thresholds) == 2
        ), "SentenceAndTargetOperation only support two inputs."

    def filter(self, sentence: str = None, target: str = None) -> bool:
        tokenized_sentence = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        tokenized_target = self.nlp(target, disable=["parser", "tagger", "ner"])

        condition1 = self.operators[0](len(tokenized_sentence), self.thresholds[0])
        condition2 = self.operators[1](len(tokenized_target), self.thresholds[1])
        return condition1 and condition2
