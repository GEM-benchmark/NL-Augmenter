from typing import List
import random
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
A tagging implementation for NER systems.
John Smith cooked a curry in the evening. --> John D. Smith cooked a curry in the evening.
"""


class LongerNamesNer(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    locales = "All"
    no_of_repeats = 1  # values should not be larger than 3-4

    def __init__(self, no_of_repeats=1):
        super().__init__()
        random.seed(self.seed)
        self.no_of_repeats = no_of_repeats

    def generate(self, token_sequence: List[str], tag_sequence: List[str]):
        tag = "PERSON" if "B-PERSON" in tag_sequence else "PER"
        b_tag = "B-" + tag
        i_tag = "I-" + tag
        if len(token_sequence) == len(tag_sequence) and b_tag in tag_sequence:
            begin = tag_sequence.index(b_tag)
            next = begin + 1
            if next < len(tag_sequence) and i_tag == tag_sequence[next]:
                for _ in range(self.no_of_repeats):
                    random_upper_letter = chr(random.randint(ord("A"), ord("Z")))
                    token_sequence.insert(next, random_upper_letter)
                    tag_sequence.insert(next, i_tag)
        return token_sequence, tag_sequence
