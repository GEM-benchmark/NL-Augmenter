import operator
import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from collections import defaultdict
from typing import Union

"""
A filter on if the tokens contain specific speech tag a certain number of times.
"""


class SpeechTagFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        speech_tags: Union[list, str] = ["NOUN", "VERB"],
        thresholds: Union[list, int] = [2, 2],
        operations: Union[list, str] = [">", ">"],
        percentages: bool = False,
    ):
        super().__init__()
        self.max_input_length = self.get_input_length(
            speech_tags, thresholds, operations
        )
        self.final_operators = self.parse_operator(operations)
        self.final_speech_tags = self.convert_scalar_to_list(speech_tags)
        self.final_thresholds = self.convert_scalar_to_list(thresholds)
        self.nlp = spacy.load("en_core_web_sm")
        self.percentages = percentages
        self.sanity_check()

    def get_input_length(self, speech_tags, thresholds, operations):
        all_inputs = [speech_tags, thresholds, operations]
        lengths = defaultdict(int)
        for key, user_input in zip(
            ["speech_tags", "thresholds", "operations"], all_inputs
        ):
            if isinstance(user_input, list):
                lengths[key] = len(user_input)
            else:
                lengths[key] = 1

        unique_lengths = set(lengths.values())
        if len(unique_lengths) == 1:
            return 1
        elif len(unique_lengths) > 2:
            raise ValueError("One or more lists given with non-matching lengths")

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
                f"Invalid Bounds: Two operations given for the same speech tag '{key}' that alternate the same bound at position '{position}'"
            )

    def sanity_check(self):
        bounds = defaultdict(lambda: [None, None])
        for curr_speech_tag, curr_threshold, curr_operator in zip(
            self.final_speech_tags, self.final_thresholds, self.final_operators
        ):
            if curr_operator == operator.gt:
                self.check_exisiting_bounds(bounds, curr_speech_tag, 0)
                bounds[curr_speech_tag][0] = curr_threshold + 1
            elif curr_operator == operator.ge:
                self.check_exisiting_bounds(bounds, curr_speech_tag, 0)
                bounds[curr_speech_tag][0] = curr_threshold
            elif curr_operator == operator.lt:
                self.check_exisiting_bounds(bounds, curr_speech_tag, 1)
                bounds[curr_speech_tag][1] = curr_threshold - 1
            elif curr_operator == operator.le:
                self.check_exisiting_bounds(bounds, curr_speech_tag, 1)
                bounds[curr_speech_tag][1] = curr_threshold
            elif curr_operator == operator.eq:
                self.check_exisiting_bounds(bounds, curr_speech_tag, 0)
                self.check_exisiting_bounds(bounds, curr_speech_tag, 1)
                bounds[curr_speech_tag][0] = curr_threshold
                bounds[curr_speech_tag][1] = curr_threshold

        for curr_speech_tag, curr_bounds in bounds.items():
            if curr_bounds[0] is None or curr_bounds[1] is None:
                continue
            if curr_bounds[0] > curr_bounds[1]:
                raise ValueError(
                    f"Invalid Bounds: The bounds for the speech tag '{curr_speech_tag}' are falsely specified and always return false since the lower bound is '{curr_bounds[0]}' and the upper bound is '{curr_bounds[1]}'"
                )

    def filter(self, sentence):
        doc = self.nlp(sentence)
        contained_speech_tags = doc.count_by(spacy.attrs.IDS["POS"])
        human_readable_tags = {}
        for pos, count in contained_speech_tags.items():
            if self.percentages:
                human_readable_tags[doc.vocab[pos].text] = (
                    100.0 * count / sum(contained_speech_tags.values())
                )
            else:
                human_readable_tags[doc.vocab[pos].text] = count

        # Go through each comparison, stop if one of them evaluates to False
        for curr_speech_tag, curr_threshold, curr_operator in zip(
            self.final_speech_tags, self.final_thresholds, self.final_operators
        ):
            if not curr_operator(human_readable_tags[curr_speech_tag], curr_threshold):
                return False

        return True
