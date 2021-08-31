import itertools
import random
import json

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

def butter_finger(text, language=None, keyboard="inscript", prob=0.1,  seed=0, max_outputs=1):

    with open('key_mapping.json','r') as f:
        key_mapping = json.load(f)

    languages = list(key_mapping.keys())

    if language not in key_mapping:
        raise Exception(f"Language not supported. Available languages: {languages}.")

    keyboards = list(key_mapping[language].keys())
    if keyboard not in key_mapping[language]:
        raise Exception(f"Keyboard not supported. Available keyboards for '{language}': {keyboards}.")

    random.seed(seed)
    key_approx = key_mapping[language][keyboard]

    prob_of_typo = int(prob * 100)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for letter in text:
            if letter not in key_approx.keys():
                new_letter = letter
            else:
                if random.choice(range(0, 100)) <= prob_of_typo:
                    new_letter = random.choice(key_approx[letter])
                else:
                    new_letter = letter

            butter_text += new_letter
        perturbed_texts.append(butter_text)
    return perturbed_texts


"""
Butter Finger implementation borrowed and edited from https://github.com/alexyorke/butter-fingers.
"""


class ButterFingersPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["hi","te","ta"]

    def __init__(self, language:str, keyboard:str, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.language = language
        self.keyboard = keyboard

    def generate(self, sentence: str, language: str):
        perturbed_texts = butter_finger(
            text=sentence,
            language=self.language,
            keyboard=self.keyboard,
            prob=0.05,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
