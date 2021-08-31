import itertools
import random
import opencc
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import shutil
import jieba
import pypinyin


def chinese_butter_finger(text,
                          prob,
                          seed,
                          max_outputs,
                          config
                          ):
    random.seed(seed)

    perturbed_texts = []

    if(config == 's2t'):
        converter = opencc.OpenCC('s2t.json')
    elif (config == 't2s'):
        converter = opencc.OpenCC('t2s.json')
    else:
        print("Configuration not specified")
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for chinese_character in text:
            if random.random() <= prob:

                new_chinese_character = converter.convert(chinese_character)
            else:
                new_chinese_character = chinese_character

            butter_text += new_chinese_character
        perturbed_texts.append(butter_text)
    return perturbed_texts




"""
Chinese Words and Characters Butter Fingers Perturbation
"""

class ChineseSimplifiedTraditionalPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]

    def __init__(self, seed=0, max_outputs=1, prob=1, config = 's2t'):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.config = config

    def generate(self, sentence: str):
        perturbed_texts = chinese_butter_finger(
            text=sentence,
            prob=self.prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            config=self.config
        )
        return perturbed_texts

if __name__ == '__main__':
    simp_text = "随着两个遗迹文明的发展，他们终于开始了争斗。遗迹之间的能量冲突是战争的导火索，因为一方出现，另一方的遗迹能量就会相应的颓落。"
    trad_text = '恰當的運用反義詞，可以形成鮮明的對比，把事物的特點表達得更充分，給人留下深刻難忘的印象。'
    perturb_func = ChineseSimplifiedTraditionalPerturbation(config='s2t')
    new_text = perturb_func.generate(simp_text)
    print(new_text)



