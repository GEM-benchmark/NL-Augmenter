import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def change_char_case(text, prob=0.1, seed=0):
    random.seed(seed)
    result = ""
    for c in text:
        if c.isupper() and random.random() < prob:
            result += c.lower()
        elif c.islower() and random.random() < prob:
            result += c.upper()
        else:
            result += c
    return result


"""
Change char cases randomly
"""


class ChangeCharCase(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = change_char_case(text=sentence, prob=0.1, seed=self.seed)
        return pertubed
