import random
import chinese2digits as c2d
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Chinese numerical words to digits
"""

class ChineseToDigits(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]
    keywords = ["morphological", "lexical", "api-based", "written", "highly-meaning-preserving"]

    # transformation_prob : the probability that the transformation is applied to the input text

    def __init__(self, seed=0, max_outputs=1, transformation_prob=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.transformation_prob = transformation_prob
        self.seed = seed
        self.max_outputs = max_outputs


    def generate(self, sentence: str):

        random.seed(self.seed)

        transfered_texts = []

        converter = opencc.OpenCC(self.converter_config)

        for _ in range(self.max_outputs):
            buffer_text = ""
            for chinese_character in sentence:
                if random.random() <= self.transformation_prob:

                    new_chinese_character = c2d.takeChineseNumberFromString(chinese_character)['replacedText']
                else:
                    new_chinese_character = chinese_character

                buffer_text += new_chinese_character
            transfered_texts.append(buffer_text)
        return transfered_texts

"""
if __name__ == '__main__':
    simp_text = "小明今年亏了十万，真糟糕！"
    trans_func = ChineseToDigits()
    new_text = trans_func.generate(simp_text)
    print(new_text)

"""

