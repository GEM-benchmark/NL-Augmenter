import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Leet speak letter perturbation based on https://simple.wikipedia.org/wiki/Leet, excluding the space > 0.
"""

leet_letter_mappings = {
    "!": "1",
    "7": "1",
    "A": "4",
    "B": "8",
    "C": "0",
    "D": "0",
    "E": "3",
    "G": "6",
    "I": "1",
    "J": "9",
    "L": "7",
    "N": "11",
    "O": "0",
    "S": "5",
    "T": "7",
    "X": "8",
    "Z": "2",
    "b": "6",
    "e": "3",
    "g": "9",
    "h": "4",
    "j": "7",
    "m": "3",
    "o": "0",
    "w": "3",
    "y": "4",
    "|": "1",
    "Θ": "0",
    "ε": "3",
    "ω": "3",
    "∈": "3",
    "∩∩": "3",
}


class LeetLetters(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]

    def __init__(self, seed: int = 0, max_outputs: int = 1, max_leet: float = 0.5) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.max_leet = max_leet

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)
        max_leet_replacements = int(self.max_leet * len(sentence))
        perturbed_texts = []
        # Perturb the input sentence max_output times
        for _ in itertools.repeat(None, self.max_outputs):
            # Determine what to replace
            leet_candidates = []
            for idx, letter in enumerate(sentence):
                if letter in leet_letter_mappings:
                    leet_candidates.append((idx, leet_letter_mappings[letter]))
            leet_replacements = random.choices(leet_candidates, k=max_leet_replacements)

            # Conduct replacement
            sentence_list = list(sentence)
            for idx, leet in leet_replacements:
                sentence_list[idx] = str(leet)
            perturbed_texts.append("".join(sentence_list))
            
        return perturbed_texts
