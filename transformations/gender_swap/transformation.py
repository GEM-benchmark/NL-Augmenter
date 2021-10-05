import random

from typing import List
from checklist.editor import Editor

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from .gender_pairs import GENDER_PAIRS


class GenderSwap(SentenceOperation):
    """Swaps all gendered words in a given sentence with their counterparts.

    Args:
        swap_names: swap names randomly? e.g Alice ↔ Bob. Defaults: True.
        seed: initial seed. Defaults: 0.
        max_outputs: maximum number of generated outputs. Defaults: 1.
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(
        self, swap_names: bool = True, seed: int = 0, max_outputs: int = 1
    ) -> None:
        super().__init__(seed, max_outputs)
        self.pairs = GENDER_PAIRS
        self.swap_names = swap_names

        if self.swap_names:
            # Random choice from a set is not possible, we'll cache the lists
            self._male_names_list = Editor().lexicons["male"]
            self._female_name_list = Editor().lexicons["female"]

            # And keep sets for a quick lookup
            self.male_names = set(map(str.lower, self._male_names_list))
            self.female_names = set(map(str.lower, self._female_name_list))

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

        # Edge case 'step-son-': --> we want 'step-son' only.
        raw = raw.strip("-")
        raw = raw.lower()

        return raw

    def generate(self, sentence: str) -> List[str]:
        output = []
        words = sentence.split(" ")

        for word in words:

            raw = self._normalize(word)

            counterpart = None

            if raw in self.pairs:
                counterpart = self.pairs[raw]

            if self.swap_names:
                if raw in self.female_names:
                    counterpart = random.choice(self._male_names_list)

                if raw in self.male_names:
                    counterpart = random.choice(self._female_name_list)

            if counterpart is not None:
                # If we found a counterpart to an original word, replace it
                y = word.lower().replace(raw, counterpart)

                # Bring back casing of the first letter
                y = self._copy_casing(word, y)

                output.append(y)
            else:
                output.append(word)

        return [" ".join(output)]
