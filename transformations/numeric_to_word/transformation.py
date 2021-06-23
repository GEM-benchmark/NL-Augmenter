import random
import string
import numeric2word

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

class NumericToWord(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = ""
        words = sentence.split()
        for word in words:
            if pertubed != "":
                pertubed += " "
            perturbed += numeric2word(word, seed=self.seed)
        return pertubed

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = Numeric2Word()
    sentence = "Please buy me 20 apples"
    test_cases = []
    for sentence in ["Please buy me 20 apples",
                     "The deadline is in 2020/01/02",
                     "I have 3 dogs at home",
                     "My phone number is +1371893178",
                     "The price is $300"]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": {"sentence": tf.generate(sentence)}}
        )
    json_file = {"type": "numeric_to_word", "test_cases": test_cases}
    # json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))

    with open("task.json", "w") as out_file:
        json.dump(json_file, out_file, indent=2, ensure_ascii=True)
"""

if __name__ == '__main__':
    import json
    # from TestRunner import convert_to_snake_case
    tf = NumericToWord()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Please buy me 20 apples",
                     "The deadline is in 2020/01/02",
                     "I have 3 dogs at home",
                     "My phone number is +1371893178",
                     "The price is $300"]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": {"sentence": tf.generate(sentence)}}
        )
    json_file = {"type": "numeric_to_word", "test_cases": test_cases}
    # json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))

    with open("task.json", "w") as out_file:
        json.dump(json_file, out_file, indent=2, ensure_ascii=True)