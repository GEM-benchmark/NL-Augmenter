import numpy as np

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class RandomUpperPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["af", "sq", "am", "eu","en", "be", "bn", "bs", "my", "ca", "ceb", "zh", "co", "hr", "nl", "cs", 'da', "eo",
                 "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", 'el', "gu", "ht", "ha", "haw", "iw", "hu", "is", "ig",
                 "ga", "it", "lb", "no", "pl", "pt", "ro", "gd", "sr", "es", "sv", "uk", "cu"]

    def __init__(self, seed=0, max_output=1, corrupt_proportion=0.1):
        super().__init__(seed)
        np.random.seed(seed)
        self.max_output = max_output
        self.corrupt_proportion = corrupt_proportion

    def generate(self, sentence: str):
        perturbed_texts = [self.random_upper(sentence) for _ in range(self.max_output)]
        return perturbed_texts

    def random_upper(self, sentence: str):
        positions = np.random.choice(range(len(sentence)), int(len(sentence) * self.corrupt_proportion), False)

        new_sentence = [
            letter if index not in positions else letter.upper()
            for index, letter in enumerate(sentence)
        ]
        return "".join(new_sentence)
