from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from .gender_pairs import GENDER_PAIRS

"""
TODO desc
"""


class GenderSwap(SentenceOperation):
    tasks = [  # TODO verify it
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed: int = 0, max_outputs: int = 1) -> None:
        super().__init__(seed, max_outputs)
        self.pairs = GENDER_PAIRS

    def _copy_casing(self, target: str, input: str) -> str:
        """Sets the first char of input to have the same case as target.

        Eg. ("Hello", "word") -> "Word".
        """
        if target[0].isupper():
            input = input[0].upper() + input[1:]

        return input

    def _normalize(self, word: str) -> str:
        """Normalize a word to contain only alphabetic characters
        (and maybe a dash, but only between letters).
        """
        raw = word.lower()

        # Edge case: "son's..." --> 'son...'. Dots will be filter out later
        raw = raw.replace("'s", "")

        # Filter all non-alphabetic and non-dash character.
        # Dash is a special case for entities like 'step-son'.
        raw = "".join(c for c in raw if c.isalpha() or c == "-").lower()

        # Edge case 'step-son-': --> we want 'step-son' ony.
        raw = raw.strip("-")
        raw = raw.lower()

        return raw

    def generate(self, sentence: str) -> List[str]:
        output = []
        words = sentence.split(" ")

        for word in words:

            raw = self._normalize(word)

            if raw in self.pairs:
                # If the word is gendered, replace it with its counterpart
                y = word.lower().replace(raw, self.pairs[raw])

                # Bring casing of the first letter back
                y = self._copy_casing(word, y)

                output.append(y)
            else:
                output.append(word)

        return [" ".join(output)]
