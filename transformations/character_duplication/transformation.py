import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def duplicate(text, prob=0.1, seed=42, max_outputs=1):
    random.seed(seed)

    original_text = list(text)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        perturbed_text = [
            [letter] if random.random() > prob else [letter, letter]
            for letter in original_text
        ]
        perturbed_text = [
            letter for sublist in perturbed_text for letter in sublist
        ]
        perturbed_texts.append("".join(perturbed_text))
    return perturbed_texts


class CharacterDuplication(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["All"]

    def __init__(self, seed=42, max_outputs=1, prob=0.1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob

    def generate(self, sentence: str):
        perturbed_texts = duplicate(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
