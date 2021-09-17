import itertools
import random
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import jieba
from nlpcda import Similarword

def chinese_antonym_synonym_substitution(text,
                          prob,
                          seed,
                          max_outputs,
                          config,
                          chinese_antonym_data
                          ):
    random.seed(seed)

    perturbed_texts = []
    word1_list = [chinese_antonym['word1'] for chinese_antonym in chinese_antonym_data]
    word2_list = [chinese_antonym['word2'] for chinese_antonym in chinese_antonym_data]

    if(config == 'synonym'):
        smw = Similarword(create_num=max_outputs+1, change_rate=prob)
        output_list = smw.replace(text)

        # Notice that the first input is the non-perturb version
        output_list = output_list[1:]
        perturbed_texts = output_list

    if(config == 'antonym'):

        output = jieba.lcut(text)
        for _ in itertools.repeat(None, max_outputs):
            butter_text = ""
            for perturb_word in output:
                perturb_antonym = []
                if(perturb_word in word1_list):
                    indices = [index for index, word1 in enumerate(word1_list) if word1 == perturb_word]
                    perturb_antonym = [word2_list[index] for index in indices]
                elif(perturb_word in word2_list):
                    indices = [index for index, word2 in enumerate(word2_list) if word2 == perturb_word]
                    perturb_antonym = [word1_list[index] for index in indices]
                else:
                    print("Word to be perturbed is not in the Chinese Antonym database")

                if random.random() <= prob and len(perturb_antonym) != 0:
                    new_chinese_character = random.choice(perturb_antonym)
                else:
                    new_chinese_character = perturb_word
                butter_text += new_chinese_character
            perturbed_texts.append(butter_text)
    return perturbed_texts

def load_chinese_antonym_data():
    dirname = os.path.dirname(__file__)
    words_list = []
    with open(os.path.join(dirname, '反义词库.txt'), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            if(line.rstrip() != ""):
                dict = {}
                word_freq = line.split("-")
                dict["word1"] = word_freq[0]
                dict["word2"] = word_freq[1].rstrip()
                words_list.append(dict)
    return words_list

"""
Chinese Words and Characters Butter Fingers Perturbation
"""

class ChineseAntonymAndSynonymSubtitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]
    keywords = ["lexical", "rule-based", "api-based", "written", "highly-meaning-preserving", "meaning-alteration", "high-precision"]

    def __init__(self, seed=0, max_outputs=1, prob=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.chinese_antonym_data = load_chinese_antonym_data()

    def generate(self, sentence: str, config : str = 'synonym'):
        perturbed_texts = chinese_antonym_synonym_substitution(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            config=config,
            chinese_antonym_data=self.chinese_antonym_data
        )
        return perturbed_texts

if __name__ == '__main__':
    simp_text = "汉字是语素文字，总数非常庞大。汉字总共有多少字？到目前为止，恐怕没人能够答得上来精确的数字。"
    perturb_func = ChineseAntonymAndSynonymSubtitution()
    # new_text = perturb_func.generate(simp_text, config = "antonym")
    new_text = perturb_func.generate(simp_text)
    print(new_text)



