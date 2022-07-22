import itertools
import random

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


def add_underscore(text, new_symbol="_", prob=0.05, seed=42, max_outputs=1):
    random.seed(seed)

    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        perturbed_text = "".join(
            [
                letter
                if letter != " " or random.random() > prob
                else new_symbol
                for letter in text
            ]
        )
        perturbed_texts.append(perturbed_text)
    return perturbed_texts


class UnderscoreTrick(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["All"]
    keywords = [
        "morphological",
        "noise",
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
    ]

    def __init__(self, seed=42, max_outputs=1, prob=0.05, new_symbol="_"):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.new_symbol = new_symbol

    def generate(self, sentence: str):
        perturbed_texts = add_underscore(
            text=sentence,
            new_symbol=self.new_symbol,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
