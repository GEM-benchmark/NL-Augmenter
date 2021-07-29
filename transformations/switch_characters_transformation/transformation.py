import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def switch_characters(text, prob=0.1, seed=0, max_outputs=1):
    random.seed(seed)
    original_text = list(text)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        perturbed_text = [original_text[0]]
        for letter in original_text[1:]:
            if random.random() <= prob:
                new_letter = perturbed_text[-1]
                perturbed_text[-1] = letter
            else:
                new_letter = letter
            perturbed_text += [new_letter]

        perturbed_texts.append("".join(perturbed_text))
    return perturbed_texts


class SwitchCharactersTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=42, max_outputs=1, prob=0.1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob

    def generate(self, sentence: str) -> List[str]:
        perturbed_texts = switch_characters(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
