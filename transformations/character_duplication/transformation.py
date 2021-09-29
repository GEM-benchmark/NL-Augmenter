import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def duplicate(text, prob=0.1, seed=42, max_outputs=1):
    """
    This function duplicates random chars (not digits) in the text string, with specified probability. It returns a list of different perturbed strings, whose length is specified by max_outputs.
    """
    random.seed(seed)

    original_text = list(text)
    perturbed_texts = []
    for _ in range(max_outputs):
        perturbed_text = [
            [letter]
            if letter.isdigit() or random.random() > prob
            else [letter, letter]
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
    ]
    languages = ["All"]
    keywords = [
        "morphological",
        "noise",
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "high-generations",
    ]

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
