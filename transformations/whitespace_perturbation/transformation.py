import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def whitespace(char, random_num, remove_prob=0.1, add_prob=0.05):
    if char.isspace() and random_num < remove_prob:
        return []
    purturbed_char = [char]
    if (not char.isspace()) and random_num < add_prob:
        purturbed_char.append(' ')

    return purturbed_char


class WhitespacePerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = [
        "ar", "ca", "cs", "da", "de", 
        "en", "eo", "es", "fi", "fr", 
        "ga", "gl", "gu", "he", "hi", 
        "id", "is", "it", "kn", "la", 
        "lt", "mr", "ms", "no", "pa", 
        "pl", "pt", "ro", "ru", "sd", 
        "sk", "sl", "sv", "sw", "ta", 
        "te", "uk", "ur", "vi" 
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        random.seed(self.seed)
        perturbed_texts = []
        for _ in range(self.max_outputs):
            perturbed_text = []
            for char in sentence:
                random_num = random.random()
                perturbed_text += whitespace(char, random_num, remove_prob=0.1, add_prob=0.05)
            perturbed_texts.append(''.join(perturbed_text))
        return perturbed_texts
