import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def whitespace(text, remove_prob=0.1, add_prob=0.05, seed=0, max_outputs=1):
    random.seed(seed)
    perturbed_texts = []
    for _ in range(max_outputs):
        perturbed_text = []
        for char in text:
            random_num = random.random()
            if char.isspace() and random_num < remove_prob:
                continue
            perturbed_text.append(char)
            if (not char.isspace()) and random_num < add_prob:
                perturbed_text.append(' ')

        perturbed_texts.append(''.join(perturbed_text))
    return perturbed_texts


class WhitespacePerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = [
        "ar", "ca", "cs", "da", "de", 
        "en", "eo", "es", "fi", "fr", 
        "ga", "gl", "he", "hi", "id", 
        "is", "it", "kn", "la", "lt", 
        "mr", "ms", "no", "pa", "pl", 
        "pt", "ro", "ru", "sd", "sk", 
        "sl", "sv", "sw", "ta", "te", 
        "uk", "ur", "vi" 
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        pertubed = whitespace(text=sentence, remove_prob=0.1, add_prob=0.05, seed=self.seed, max_outputs=self.max_outputs)
        return pertubed
