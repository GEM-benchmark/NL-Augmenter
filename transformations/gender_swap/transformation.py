from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from .gender_pairs import GENDER_PAIRS

"""
TODO desc
"""

class GenderSwap(SentenceOperation):
    tasks = [ # TODO verify it
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self) -> None:
        super().__init__()
        self.pairs = GENDER_PAIRS

    def generate(self, sentence: str) -> List[str]:
        output = []
        words = sentence.split(' ')

        for word in words:
            # Filter all non-alphabetic chars in word and then lowercase
            raw = ''.join(c for c in word if c.isalpha()).lower()

            if raw in self.pairs:
                # If the word is gendered, replace it with its counterpart
                y = word.lower()
                y = y.replace(raw, self.pairs[raw])
                output.append(y)
            else:
                output.append(word)

        return [' '.join(output)]


if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    gs = GenderSwap()
    y = gs._get_pairs()

    print(y)