import random
import opencc
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType



def chinese_simplified_traditional_perturbation(text,
                          transformation_prob,
                          seed,
                          max_outputs,
                          converter_config
                          ):
    random.seed(seed)

    perturbed_texts = []

    converter = opencc.OpenCC(converter_config)

    for _ in range(max_outputs):
        butter_text = ""
        for chinese_character in text:
            if random.random() <= transformation_prob:

                new_chinese_character = converter.convert(chinese_character)
            else:
                new_chinese_character = chinese_character

            butter_text += new_chinese_character
        perturbed_texts.append(butter_text)
    return perturbed_texts




"""
Chinese Simplified/Traditional Perturbation
"""

class ChineseSimplifiedTraditionalPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]
    keywords = ["morphological", "lexical", "api-based", "written", "highly-meaning-preserving"]

    # transformation_prob : the probability that the transformation is applied to the input text
    # converter_config : the type of conversion that you would like to do. The list of options are available in the README.md or in this link: https://github.com/BYVoid/OpenCC

    def __init__(self, seed=0, max_outputs=1, transformation_prob=1, converter_config ='s2t.json'):
        super().__init__(seed, max_outputs=max_outputs)
        self.transformation_prob = transformation_prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.converter_config = converter_config

    def generate(self, sentence: str):
        perturbed_texts = chinese_simplified_traditional_perturbation(
            text=sentence,
            transformation_prob=self.transformation_prob,
            seed=self.seed,
            max_outputs=self.max_outputs,
            converter_config=self.converter_config
        )
        return perturbed_texts

if __name__ == '__main__':
    simp_text = "hello, 随着两个遗迹文明的发展，他们终于开始了争斗。遗迹之间的能量冲突是战争的导火索，因为一方出现，另一方的遗迹能量就会相应的颓落。"
    trad_text = '恰當的運用反義詞，可以形成鮮明的對比，把事物的特點表達得更充分，給人留下深刻難忘的印象。'
    perturb_func = ChineseSimplifiedTraditionalPerturbation(converter_config='s2t.json')
    new_text = perturb_func.generate(simp_text)
    print(new_text)



