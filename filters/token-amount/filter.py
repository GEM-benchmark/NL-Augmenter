import operator
import spacy

from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from tasks.TaskTypes import TaskType
from collections import defaultdict
from typing import Union

"""
A filter on if the tokens contain specific keywords a certain number of times.
"""


class TokenAmountFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        keywords: Union[list, str] = None,
        thresholds: Union[list, str] = None,
        operations: Union[list, str] = None,
    ):
        super().__init__()
        self.max_input_length = self.get_input_length(keywords, thresholds, operations)
        self.final_operators = self.parse_operator(operations)
        self.final_keywords = self.convert_scalar_to_list(keywords)
        self.final_thresholds = self.convert_scalar_to_list(thresholds)
        self.nlp = spacy.load("en_core_web_sm")

    def get_input_length(self, keywords, thresholds, operations):
        all_inputs = [keywords, thresholds, operations]
        lengths = defaultdict(int)
        for user_input in all_inputs:
            if isinstance(user_input, list):
                lengths[len(user_input)] += 1

        if len(list(lengths.keys())) > 1:
            raise ValueError("One or more lists given with non-matching lengths")

        return list(lengths.keys())[0]

    def convert_scalar_to_list(self, pos_scalar):
        return (
            pos_scalar
            if isinstance(pos_scalar, list)
            else [pos_scalar for _ in range(self.max_input_length)]
        )

    def parse_operator(self, op):
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "==": operator.eq,
        }
        return (
            [ops[curr_operator] for curr_operator in op]
            if isinstance(op, list)
            else [ops[op] for _ in range(self.max_input_length)]
        )

    def filter(self, sentence):
        tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        contained_keywords = defaultdict(int)
        for token in tokenized:
            contained_keywords[token.text] += 1

        # Go through each comparison, stop if one of them evaluates to False
        for curr_keyword, curr_threshold, curr_operator in zip(
            self.final_keywords, self.final_thresholds, self.final_operators
        ):
            if not curr_operator(contained_keywords[curr_keyword], curr_threshold):
                return False

        return True
