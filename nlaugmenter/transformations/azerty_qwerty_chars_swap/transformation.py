import numpy as np

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class AzertyQwertyCharsSwap(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "morphological",
        "noise",
        "rule-based",
        "unnaturally-sounding",
        "unnaturally-written",
        "highly-meaning-preserving",
        "high-coverage",
        "high-precision",
    ]

    def __init__(self, seed=0, percent_swap=0.2, max_outputs=1):
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.percent_swap = percent_swap
        self.swap_dict = {"q": "a", "w": "z", "a": "q", "z": "w", "y": "z"}

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        new_sentences = []
        for _ in range(self.max_outputs):
            new_sentence = ""
            for char in sentence:
                if (
                    char.lower() in self.swap_dict
                    and np.random.uniform() < self.percent_swap
                ):
                    new_char = self.swap_dict[char.lower()]
                    if char.isupper():
                        new_char = new_char.upper()
                    new_sentence += new_char
                else:
                    new_sentence += char
            new_sentences.append(new_sentence)

        return new_sentences
