import itertools
import random
import unidecode as u
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

def chinese_butter_finger(text, chinese_character_database, prob=0.3, keyboard="pinyin", seed=0, max_outputs=1):
    random.seed(seed)

    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for chinese_character in text:
            similar_pinyins = get_characters_with_similar_pinyin(chinese_character, chinese_character_database, keyboard)

            if random.random() <= prob and similar_pinyins != "":
                new_chinese_character = random.choice(similar_pinyins)
            else:
                new_chinese_character = chinese_character

            butter_text += new_chinese_character
        perturbed_texts.append(butter_text)
    return perturbed_texts

def get_characters_with_similar_pinyin(chinese_character, chinese_character_database, keyboard):

    pinyin_for_char_to_be_perturbed = ""
    if keyboard == "pinyin":
        for char_dict in chinese_character_database:
            if(chinese_character == char_dict['word']):
                pinyin_for_char_to_be_perturbed = char_dict['pinyin']

        chars_with_similar_pinyin = ""
        for char_dict in chinese_character_database:
            if(u.unidecode(pinyin_for_char_to_be_perturbed) == u.unidecode(char_dict['pinyin'])):
                chars_with_similar_pinyin += char_dict['word']
    else:
        print("Keyboard not supported.")

    return chars_with_similar_pinyin


def load_chinese_character_data_into_memory():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "chinese_word.json")
    with open(filepath) as file:
        chinese_character_database = json.load(file)
    return chinese_character_database


"""
Chinese Characters Butter Fingers Perturbation
"""

class ChineseButterFingersPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]

    def __init__(self, seed=0, max_outputs=1, prob=0.1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.chinese_character_database = load_chinese_character_data_into_memory()

    def generate(self, sentence: str):
        perturbed_texts = chinese_butter_finger(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            chinese_character_database = load_chinese_character_data_into_memory()
        )
        return perturbed_texts

