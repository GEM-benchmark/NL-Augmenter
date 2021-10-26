import operator
from collections import defaultdict
from typing import Union

import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
A filter on if the tokens contain specific keywords a certain number of times.
"""


class TokenAmountFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        keywords: Union[list, str] = None,
        thresholds: Union[list, int] = None,
        operations: Union[list, str] = None,
    ):
        super().__init__()
        self.max_input_length = self.get_input_length(
            keywords, thresholds, operations
        )
        self.final_operators = self.parse_operator(operations)
        self.final_keywords = self.convert_scalar_to_list(keywords)
        self.final_thresholds = self.convert_scalar_to_list(thresholds)
        self.nlp = spacy.load("en_core_web_sm")
        self.sanity_check()

    def get_input_length(self, keywords, thresholds, operations):
        all_inputs = [keywords, thresholds, operations]
        lengths = defaultdict(int)
        for key, user_input in zip(
            ["keywords", "thresholds", "operations"], all_inputs
        ):
            if isinstance(user_input, list):
                lengths[key] = len(user_input)
            else:
                lengths[key] = 1

        unique_lengths = set(lengths.values())
        if unique_lengths == {1}:
            return 1
        elif len(unique_lengths) > 2:
            raise ValueError(
                "One or more lists given with non-matching lengths"
            )

        return max(unique_lengths)

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

    @staticmethod
    def check_exisiting_bounds(bounds, key, position):
        if bounds[key][position] is not None:
            raise ValueError(
                f"Invalid Bounds: Two operations given for the same keyword '{key}' that alternate the same bound at position '{position}'"
            )

    def sanity_check(self):
        bounds = defaultdict(lambda: [None, None])
        for curr_keyword, curr_threshold, curr_operator in zip(
            self.final_keywords, self.final_thresholds, self.final_operators
        ):
            if curr_operator == operator.gt:
                self.check_exisiting_bounds(bounds, curr_keyword, 0)
                bounds[curr_keyword][0] = curr_threshold + 1
            elif curr_operator == operator.ge:
                self.check_exisiting_bounds(bounds, curr_keyword, 0)
                bounds[curr_keyword][0] = curr_threshold
            elif curr_operator == operator.lt:
                self.check_exisiting_bounds(bounds, curr_keyword, 1)
                bounds[curr_keyword][1] = curr_threshold - 1
            elif curr_operator == operator.le:
                self.check_exisiting_bounds(bounds, curr_keyword, 1)
                bounds[curr_keyword][1] = curr_threshold
            elif curr_operator == operator.eq:
                self.check_exisiting_bounds(bounds, curr_keyword, 0)
                self.check_exisiting_bounds(bounds, curr_keyword, 1)
                bounds[curr_keyword][0] = curr_threshold
                bounds[curr_keyword][1] = curr_threshold

        for curr_keyword, curr_bounds in bounds.items():
            if curr_bounds[0] is None or curr_bounds[1] is None:
                continue
            if curr_bounds[0] > curr_bounds[1]:
                raise ValueError(
                    f"Invalid Bounds: The bounds for the keyword '{curr_keyword}' are falsely specified and always return false since the lower bound is '{curr_bounds[0]}' and the upper bound is '{curr_bounds[1]}'"
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
            if not curr_operator(
                contained_keywords[curr_keyword], curr_threshold
            ):
                return False

        return True
