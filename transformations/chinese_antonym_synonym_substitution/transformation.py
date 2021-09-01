import itertools
import random
import opencc
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import jieba
from nlpcda import Similarword

def chinese_antonym_synonym_substitution(text,
                          prob,
                          seed,
                          max_outputs,
                          config
                          ):
    random.seed(seed)

    perturbed_texts = []
    if(config == 'synonym'):
        smw = Similarword(create_num=max_outputs+1, change_rate=prob)
        output_list = smw.replace(text)

        # Notice that the first input is the non-perturb version
        output_list = output_list[1:]
        perturbed_texts = output_list


    if(config == 'antonym'):
        print("placeholder")
    # for _ in itertools.repeat(None, max_outputs):
    #     if (config == 'synonym'):
    #
    #         text = smw.replace(text)
    #
    #     perturbed_texts.append(butter_text)
    return perturbed_texts




"""
Chinese Words and Characters Butter Fingers Perturbation
"""

class ChineseAntonymAndSynonymSubtitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]

    def __init__(self, seed=0, max_outputs=1, prob=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs

    def generate(self, sentence: str, config : str = 'synonym'):
        perturbed_texts = chinese_antonym_synonym_substitution(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            config=config
        )
        return perturbed_texts

if __name__ == '__main__':
    simp_text = "随着两个遗迹文明的发展，他们终于开始了争斗。遗迹之间的能量冲突是战争的导火索，因为一方出现，另一方的遗迹能量就会相应的颓落。"
    perturb_func = ChineseAntonymAndSynonymSubtitution()
    new_text = perturb_func.generate(simp_text)
    print(new_text)



