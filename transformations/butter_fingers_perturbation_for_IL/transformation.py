import os
import itertools
import random
import json

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

'''
    This transformation adds noise to all types of text sources (sentence, paragraph, etc.), which is proportional to noise erupting from keyboard typos resulting in common spelling errors. 
    We have expanded the existing implementation for English (source) to a few Indian Languages:
    1. Bangla ('bn'), 
    2. Gujarati ('gu'), 
    3. Hindi ('hi'), 
    4. Kannada ('kn'), 
    5. Malayalam ('ml'), 
    6. Oriya ('or'), 
    7. Punjabi ('pa'), 
    8. Tamil ('ta'), 
    9. Telugu ('te')

    args:
        language (str): base language for butter fingers
        keyboard (str): preffered keyboard schema (currently available: "inscript")
        seed (int, default = 0): seed for reproducibility 
'''

def butter_finger(text, key_approx, prob=0.1,  seed=0, max_outputs=1):

    random.seed(seed)
    
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


class ButterFingersPerturbationForIL(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]

    keywords = ["morphological", "noise", "rule-based", "high-coverage", "high-precision",
                "unnatural-sounding", "unnaturally-written", "high-generations"]

    languages = ['bn','gu','hi','kn','ml','or','pa','ta','te']

    language_mapping = {"bengali":'bn',
                        "gujarati":'gu',
                        "hindi":'hi',
                        "kannada":'kn',
                        "malayalam":'ml',
                        "oriya":'or',
                        "punjabi":'pa',
                        "tamil":'ta',
                        "telugu":'te',}

    def __init__(self, language:str, keyboard:str, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.language = language
        self.keyboard = keyboard

        mapping_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key_mapping.json')

        with open(mapping_path,'r') as f:
            self.key_mapping = json.load(f)

        languages = list(self.key_mapping.keys())

        if language not in self.key_mapping:
            raise Exception(f"Language not supported. Available languages: {languages}.")

        keyboards = list(self.key_mapping[language].keys())
        if keyboard not in self.key_mapping[language]:
            raise Exception(f"Keyboard not supported. Available keyboards for '{language}': {keyboards}.")

        self.key_approx = self.key_mapping[language][keyboard]

    @staticmethod
    def get_language_mapping(self):
        return self.language_mapping

    def generate(self, sentence:str):
        perturbed_texts = butter_finger(
            text=sentence,
            key_approx = self.key_approx,
            prob=0.05,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
