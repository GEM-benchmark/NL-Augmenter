import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

def change_char_case(text, prob=0.1, max_outputs=1):
    results = []
    for _ in range(max_outputs):
        result = []
        for c in text:
            if c.isupper() and random.random() < prob:
                result.append(c.lower())
            elif c.islower() and random.random() < prob:
                result.append(c.upper())
            else:
                result.append(c)
        result = "".join(result)
        results.append(result)
    return results


"""
Change char cases randomly
"""


class ChangeCharCase(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, max_outputs=1):
        super().__init__(max_outputs=max_outputs)

    def generate(self, sentence: str):
        perturbed = change_char_case(
            text=sentence, prob=0.1, max_outputs=self.max_outputs
        )
        return perturbed
