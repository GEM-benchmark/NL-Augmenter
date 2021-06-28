import itertools
import random
import numpy as np
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

def random_deletion(text, prob=0.1):
    text = np.array(text.split())
    N = len(text)
    mask = np.random.binomial(1, 1-prob, N) == 1
    text_tf = text[mask]
    text_tf = " ".join(text_tf)
    text_tf = text_tf if len(text_tf) > 0 else text[random.randint(0,N-1)]
    return [text_tf]

"""
Butter Finger implementation borrowed from https://github.com/alexyorke/butter-fingers.
"""


class RandomDeletion(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, prob=0.25, seed=0):
        super().__init__()
        random.seed(seed)
        np.random.seed(seed)
        self.prob = prob

    def generate(self, sentence: str):
        perturbed_texts = random_deletion(
            text=sentence, prob=self.prob
        )
        return perturbed_texts
