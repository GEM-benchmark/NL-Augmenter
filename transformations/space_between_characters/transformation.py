import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def add_spaces(text, prob=0.1, seed=0, max_outputs=1):
    random.seed(seed)

    words = text.split(" ")
    perturbed_texts = []
    for _ in range(max_outputs):
        perturbed_text = []
        for word in words:
            if random.random() <= prob:
                new_word = " ".join(word)
            else:
                new_word = word
            perturbed_text.append(new_word)
        perturbed_texts.append(" ".join(perturbed_text))
    return perturbed_texts


class SpaceBetweenCharacters(SentenceOperation):
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
        perturbed_texts = add_spaces(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
