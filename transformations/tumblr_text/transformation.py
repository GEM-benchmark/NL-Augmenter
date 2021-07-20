import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Implement tumblr-text, e.g. 'foo bar' -> 'f o o   b a r'
"""


class TumblrText(SentenceOperation):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def generate(self, sentence: str):
        return " ".join(sentence)
