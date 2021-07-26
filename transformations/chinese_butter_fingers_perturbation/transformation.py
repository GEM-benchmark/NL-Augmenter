import itertools
import random
import unidecode as u
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def butter_finger(text, prob=0.1, keyboard="pinyin", seed=0, max_outputs=1):
    random.seed(seed)
    key_approx = {}
    dirname = os.path.dirname(__file__)
    print(dirname)
    filepath = os.path.join(dirname, 'chinese_word.json')

    print(filepath)
    with open(filepath) as file:
        chinese_word_database = json.load(file)

    # print(chinese_word_database)

    testChar = '啊'
    key_approx_chinese = {}
    pinyin_for_word_to_be_perturbed = ''
    if keyboard == "pinyin":
        for word_dict in chinese_word_database:
            if(testChar == word_dict['word']):
                # print(word_dict)
                print(word_dict['pinyin'])
                print(u.unidecode(word_dict['pinyin']))
                pinyin_for_word_to_be_perturbed = word_dict['pinyin']

        similar_words = ''
        for word_dict in chinese_word_database:
            if(u.unidecode(pinyin_for_word_to_be_perturbed) == u.unidecode(word_dict['pinyin'])):
                similar_words += word_dict['word']

    else:
        print("Keyboard not supported.")

    print(similar_words)

    # if keyboard == "pinyin":
    #     key_approx["妈"] = "马吗嘛骂"
    #     key_approx["他"] = "塔踏塌嗒"
    #     key_approx["q"] = "qwasedzx"
    #     key_approx["q"] = "qwasedzx"
    #     key_approx["w"] = "wqesadrfcx"
    #     key_approx["e"] = "ewrsfdqazxcvgt"
    #     key_approx["r"] = "retdgfwsxcvgt"
    #     key_approx["t"] = "tryfhgedcvbnju"
    #     key_approx["y"] = "ytugjhrfvbnji"
    #     key_approx["u"] = "uyihkjtgbnmlo"
    #     key_approx["i"] = "iuojlkyhnmlp"
    #     key_approx["o"] = "oipklujm"
    #     key_approx["p"] = "plo['ik"
    #
    #     key_approx[" "] = " "
    # else:
    #     print("Keyboard not supported.")

    prob_of_typo = int(prob * 100)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for lcletter in text:
            if lcletter not in key_approx.keys():
                new_letter = lcletter
            else:
                if random.choice(range(0, 100)) <= prob_of_typo:
                    new_letter = random.choice(key_approx[lcletter])
                else:
                    new_letter = lcletter
            butter_text += new_letter
        perturbed_texts.append(butter_text)
    # return perturbed_texts

    return ''

def get_words_with_similar_pinyin():
    print('test')

"""
Butter Finger implementation borrowed from https://github.com/alexyorke/butter-fingers.
"""


class ChineseButterFingersPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1, prob=0.1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob

    def generate(self, sentence: str):
        perturbed_texts = butter_finger(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts

