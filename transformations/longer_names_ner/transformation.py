from typing import List
import random
from interfaces.TaggingTransformation import TaggingTransformation
from tasks.TaskTypes import TaskType

"""
A tagging implementation for NER systems.
John Smith cooked a curry in the evening. --> John D. Smith cooked a curry in the evening.
"""


class LongerNamesNer(TaggingTransformation):
    tasks = [TaskType.TEXT_TAGGING]
    locales = "All"
    no_of_repeats = 1  # values should not be larger than 3-4

    def __init__(self):
        super().__init__()
        random.seed(1)

    def generate(self, token_sequence: List[str], tag_sequence: List[str]):
        if len(token_sequence) == len(tag_sequence) and "B-PER" in tag_sequence:
            begin = tag_sequence.index("B-PER")
            next = begin + 1
            if next < len(tag_sequence) and "I-PER" == tag_sequence[next]:
                for _ in range(self.no_of_repeats):
                    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
                    token_sequence.insert(next, random_upper_letter)
                    tag_sequence.insert(next, "I-PER")
        return token_sequence, tag_sequence
