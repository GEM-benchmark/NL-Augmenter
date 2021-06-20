import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def whitespace(text, remove_prob=0.1, add_prob=0.05, seed=0):
    random.seed(seed)
    newtext = ''
    for char in text:
        random_num = random.random()
        if char.isspace() and random_num < remove_prob:
            continue
        newtext += char
        if (not char.isspace()) and random_num < add_prob:
            newtext += ' '

    return newtext


class WhitespacePerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = whitespace(text=sentence, remove_prob=0.1, add_prob=0.05, seed=self.seed)
        return pertubed
