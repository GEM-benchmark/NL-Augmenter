import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Modify date formats with perturbations.
"""



class DateFormat(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]

    def __init__(self, seed: int = 0) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        # Find parts of sentence that can be perturbed

        # Perform the perturbation
        return perturbed_sentece
