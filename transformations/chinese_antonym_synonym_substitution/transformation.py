import itertools
import random
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import jieba
from nlpcda import Similarword

def chinese_antonym_substitution(text,
                          prob,
                          chinese_antonym_data
                          ):


    perturb_list = []
    for perturb_word in text:
        perturb_antonym = []

        if perturb_word not in chinese_antonym_data.keys():
            print("Word to be perturbed is not in the Chinese Antonym database")
        else:
            perturb_antonym = chinese_antonym_data[perturb_word]

        if random.random() <= prob and len(perturb_antonym) != 0:
            new_chinese_character = random.choice(perturb_antonym)
        else:
            new_chinese_character = perturb_word
        perturb_list.append(new_chinese_character)

    perturb_text = ''.join(perturb_list)
    return perturb_text

def load_chinese_antonym_data():
    dirname = os.path.dirname(__file__)
    antonym_dict = {}
    with open(os.path.join(dirname, '反义词库.txt'), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            if(line.rstrip() != ""):
                antonym_list = []
                word_antonym = line.split("-")
                new_antonym = word_antonym[1].rstrip()
                if(word_antonym[0] in antonym_dict.keys()):

                    values = antonym_dict[word_antonym[0]]

                    for value in values:
                        antonym_list.append(value)
                    if(new_antonym not in values):
                        antonym_list.append(new_antonym)
                    antonym_dict[word_antonym[0]] = antonym_list

                else:
                    antonym_list.append(word_antonym[1].rstrip())
                    antonym_dict[word_antonym[0]] = antonym_list

    return antonym_dict

"""
Chinese Antonym And Synonym Substitution
"""

class ChineseAntonymAndSynonymSubtitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]
    keywords = ["lexical", "rule-based", "api-based", "written", "highly-meaning-preserving", "meaning-alteration", "high-precision"]

    def __init__(self, seed=0, max_outputs=1, prob=0.5):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.chinese_antonym_data = load_chinese_antonym_data()

    def generate(self, sentence: str, config : str = 'synonym'):
        random.seed(self.seed)
        perturbed_texts = []
        if (config == 'synonym'):
            smw = Similarword(create_num=self.max_outputs + 1, change_rate=self.prob)
            output_list = smw.replace(sentence)

            # Notice that the first input is the non-perturb version
            output_list = output_list[1:]
            perturbed_texts = output_list

        elif (config == 'antonym'):
            output = jieba.lcut(sentence)
            for _ in itertools.repeat(None, self.max_outputs):
                perturbed_text = chinese_antonym_substitution(
                    text=output,
                    prob=self.prob,
                    chinese_antonym_data=self.chinese_antonym_data
                )
            perturbed_texts.append(perturbed_text)
        return perturbed_texts

"""
if __name__ == '__main__':
    simp_text = "汉字是语素文字，总数非常庞大。汉字总共有多少字？到目前为止，恐怕没人能够答得上来精确的数字。"
    perturb_func = ChineseAntonymAndSynonymSubtitution()
    new_text = perturb_func.generate(simp_text, config = "antonym")
    # new_text = perturb_func.generate(simp_text)
    print(new_text)


"""
