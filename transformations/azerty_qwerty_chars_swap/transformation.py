import numpy as np
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class AzertyQwertyCharsSwap(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, percent_swap=0.2):
        super().__init__(seed)
        self.percent_swap = percent_swap
        self.swap_dict = {"q": "a", "w": "z", "a": "q", "z": "w", "y": "z"}

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        new_sentence = ""
        for char in sentence:
            if char.lower() in self.swap_dict and np.random.uniform() < self.percent_swap:
                new_char = self.swap_dict[char.lower()]
                if char.isupper():
                    new_char = new_char.upper()
                new_sentence += new_char
            else:
                new_sentence += char

        return [new_sentence]
