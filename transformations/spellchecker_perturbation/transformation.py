import random

import enchant

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def is_case_same(char_1: str, char_2: str) -> bool:
    if (char_1.isupper() and char_2.isupper()) or (
        char_1.islower() and char_2.islower()
    ):
        return True
    else:
        return False


class SpellCheckerPerturbation(SentenceOperation):
    """
    Spell-checker based pertubation
    --------
    Replace words in text given a specified probability using a spell-checker
    via pyenchant library to generate similar words with spelling variations.
    This can make the model adapt to noise via randomly incorrect words.
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed: int = 0, language: str = "en_GB"):
        super().__init__(seed)
        self._spell_checker = enchant.Dict(language)

    def generate(self, sentence: str, probability: float = 0.1) -> str:
        """
        Perturbs the words in given input text using a spell-checker
        based on specified probability
        # Parameters
        sentence : `str`
            Input text
        probability : `float`, optional (default = 0.1)
            Probability of the words in input text that need to be perturbed
        # Returns
        perturbed_text: `str`
            A string containing perturbed text
        """
        split_text = sentence.split()
        for idx, word in enumerate(split_text):
            if random.random() <= probability:
                candidates = self._spell_checker.suggest(word)
                # Pick one suggestion randomly from top-5 candidates from the spell-checker suggestions
                replacement = random.choice(candidates[:5])
                if (
                    replacement
                    and replacement != word
                    and is_case_same(replacement, word)
                ):
                    split_text[idx] = replacement
        perturbed_text: str = " ".join(split_text)
        return perturbed_text


"""
For generating JSON file containing test-cases, run the file named 'test_case_generator.py' in this folder.
For references, check README.md
"""
