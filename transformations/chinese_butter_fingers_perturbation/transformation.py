import itertools
import random
import unidecode as u
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import shutil
import jieba
# from pypinyin import pinyin, lazy_pinyin
import pypinyin

if __name__ == "__main__":
    chinese_char_path = '/Users/admintmun/dev/NL-Augmenter/transformations/chinese_butter_fingers_perturbation/chinese_word.json'

    data = []
    with open(os.path.join('/Users/admintmun/dev/NL-Augmenter/transformations/chinese_butter_fingers_perturbation/',
                           'common_chinese_word.json'), mode='w', encoding='utf8') as out:
        with open(os.path.join('/Users/admintmun/dev/NL-Augmenter/transformations/chinese_butter_fingers_perturbation/',
                               '3500常用汉字.txt'), mode='r', encoding='utf8') as all:
            common_chinese_words = all.read()
            print(common_chinese_words)
            with open(chinese_char_path) as json_file:
                chinese_char_json = json.load(json_file)
                # common_chinese_words = all.read()

                for char_dict in chinese_char_json:

                    if char_dict['word'] in common_chinese_words:
                        print("common")
                        print(char_dict['word'])
                        data.append(char_dict)
        json.dump(data, out, ensure_ascii=False)
        print(data)
    text = "恰当的运用反义词，可以形成鲜明的对比，把事物的特点表达得更充分，给人留下深刻难忘的印象"

    # output = jieba.lcut(text)
    # print(output)
    # for word in output:
    #     print(word)
    #
    #     pinyin = pypinyin.pinyin(word)
    #     print(pinyin)

def chinese_butter_finger(text, chinese_character_database, common_chinese_character_database, prob, rare_word_prob, seed, max_outputs, consider_tone):
    random.seed(seed)

    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for chinese_character in text:
            similar_pinyins = get_characters_with_similar_pinyin(chinese_character, rare_word_prob, chinese_character_database, common_chinese_character_database, consider_tone)

            if random.random() <= prob and similar_pinyins != "":
                new_chinese_character = random.choice(similar_pinyins)
            else:
                new_chinese_character = chinese_character

            butter_text += new_chinese_character
        perturbed_texts.append(butter_text)
    return perturbed_texts

def get_characters_with_similar_pinyin(chinese_character, rare_word_prob, chinese_character_database, common_chinese_character_database, consider_tone):

    pinyin_for_char_to_be_perturbed = ""
    for char_dict in chinese_character_database:
        if(chinese_character == char_dict['word']):
            pinyin_for_char_to_be_perturbed = char_dict['pinyin']

    chars_with_similar_pinyin = ""
    if random.random() <= rare_word_prob:
        chars_with_similar_pinyin = retrieve_from_database(chars_with_similar_pinyin, chinese_character_database,
                                                           consider_tone, pinyin_for_char_to_be_perturbed)
    else:
        chars_with_similar_pinyin = retrieve_from_database(chars_with_similar_pinyin, common_chinese_character_database,
                                      consider_tone, pinyin_for_char_to_be_perturbed)

    return chars_with_similar_pinyin


def retrieve_from_database(chars_with_similar_pinyin, chinese_character_database, consider_tone,
                           pinyin_for_char_to_be_perturbed):
    for char_dict in chinese_character_database:
        if (consider_tone):
            if (pinyin_for_char_to_be_perturbed == char_dict['pinyin']):
                chars_with_similar_pinyin += char_dict['word']
        else:
            if (u.unidecode(pinyin_for_char_to_be_perturbed) == u.unidecode(char_dict['pinyin'])):
                chars_with_similar_pinyin += char_dict['word']
    return chars_with_similar_pinyin


def load_chinese_character_data_into_memory():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "chinese_word.json")
    with open(filepath) as file:
        chinese_character_database = json.load(file)
    return chinese_character_database

def load_common_chinese_character_data_into_memory():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "common_chinese_word.json")
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

    def __init__(self, seed=0, max_outputs=1, prob=0.3, rare_word_prob = 0.1, consider_tone = False):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.rare_word_prob = rare_word_prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.chinese_character_database = load_chinese_character_data_into_memory()
        self.common_chinese_character_database = load_common_chinese_character_data_into_memory()
        self.consider_tone = consider_tone

    def generate(self, sentence: str):
        perturbed_texts = chinese_butter_finger(
            text=sentence,
            chinese_character_database=self.chinese_character_database,
            common_chinese_character_database=self.common_chinese_character_database,
            prob=self.prob,
            rare_word_prob = self.rare_word_prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            consider_tone = self.consider_tone
        )
        return perturbed_texts

