import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import nltk

nltk.download("punkt")  # required for sent_tokenize
from nltk.tokenize import sent_tokenize
import random

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def sentence_reordering(text, seed):
    random.seed(seed)
    text_split = sent_tokenize(text)
    random.shuffle(text_split)
    return " ".join(text_split)


"""
Shuffle sentence order
"""


class SentenceReordering(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = sentence_reordering(text=sentence, seed=self.seed)
        return pertubed
