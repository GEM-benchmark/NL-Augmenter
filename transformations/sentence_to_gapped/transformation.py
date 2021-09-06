import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

import homophones_list

"""
Homophone perturbation
"""

class SentenceToGapped(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]

    def __init__(self, seed: int = 0) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)

        # Determine what to replace

        # Single-predicate gaps

        # Contiguous predicate-argument gap

        # Non-contiguous
        words = sentence.split(" ")
        for w_i, w in enumerate(words):
            for h_i, homophone_set in enumerate(homophones_list):
                if w in homophone_set:
                    # Replace with something that isn't w
                    while words[w_i] == w:
                        words[w_i] = random.choice(homophone_set)



            
        return ' '.join(words)
