import operator
import spacy

from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
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
        speech_tags: Union[list, str],
        thresholds: Union[list, str],
        operations: Union[list, str],
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

    def get_input_length(self, speech_tags, thresholds, operations):
        all_inputs = [speech_tags, thresholds, operations]
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
