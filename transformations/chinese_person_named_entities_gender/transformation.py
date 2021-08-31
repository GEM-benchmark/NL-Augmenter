import itertools
import random
import opencc
import os
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import jieba



def chinese_person_named_entities_gender(text,
                                         prob,
                                         seed,
                                         max_outputs,
                                         gender_change,
                                         chinese_names_data
                                         ):
    random.seed(seed)

    perturbed_texts = []
    print(chinese_names_data)
    # if(gender_change):
    #     converter = opencc.OpenCC('s2t.json')
    # else:
    #     print("Configuration not specified")
    # for _ in itertools.repeat(None, max_outputs):
    #     butter_text = ""
    #     for chinese_character in text:
    #         if random.random() <= prob:
    #
    #             new_chinese_character = converter.convert(chinese_character)
    #         else:
    #             new_chinese_character = chinese_character
    #
    #         butter_text += new_chinese_character
    #     perturbed_texts.append(butter_text)
    return perturbed_texts


def load_chinese_names_data():
    dirname = os.path.dirname(__file__)
    names_list = []
    with open(os.path.join(dirname, 'Chinese_Names_Corpus_Gender（120W）.txt'), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            if(line.rstrip() != ""):
                names_dict = {}
                name = line.split(",")
                names_dict["name"] = name[0]
                names_dict["gender"] = name[1].rstrip()
                names_list.append(names_dict)

    return names_list


"""
Chinese Words and Characters Butter Fingers Perturbation
"""

class ChinesePersonNamedEntitiesAndGender(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]

    def __init__(self, seed=0, max_outputs=1, prob=1, gender_change = False):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.gender_change = gender_change
        self.chinese_names_data = load_chinese_names_data()

    def generate(self, sentence: str):
        perturbed_texts = chinese_person_named_entities_gender(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            gender_change=self.gender_change,
            chinese_names_data=self.chinese_names_data
        )
        return perturbed_texts

if __name__ == '__main__':
    text = "随着两个遗迹文明的发展，阿朝他们终于开始了争斗。遗迹之间的能量冲突是战争的导火索，因为一方出现，另一方的遗迹能量就会相应的颓落。"
    short_text = '阿朝'
    perturb_func = ChinesePersonNamedEntitiesAndGender()
    new_text = perturb_func.generate(text)
    print(new_text)



