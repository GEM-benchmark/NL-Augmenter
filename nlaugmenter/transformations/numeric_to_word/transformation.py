from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

from .numeric2word import recognize_transform


class NumericToWord(SentenceOperation):
    """
    This transformation translates numeric string in major formats
    n the text into its words form. It can be used to introduce
    the number as a character token to the model.

    Please refer to the test.json for all of the test cases catered.

    This transformation translates numbers in numeric form form
    written amongst the texts for:
    - General numbers
        - general number (commas, thousands)
        - sticky numbers (2x, 5th, 8pm, 10%)
        - negatives (-0.5)
        - percentage
        - natural log (e(9))
        - fraction
        - long number
        - long number with stripes
        - sticky ranges ( (1-2) )
        - range not sticky ( ( 1-2 ) )
        - math formula equality
        - mathematical power of ten (10-4)
        - numeric in begin end bracket ( (34) )
        - numeric beside end bracket ( 34) )
        - numeric in math_bracket
        - special numbers (911)
        - currency (with the currency symbols and cents)
        - and more ..
    - Datetime
        - incomplete_date
            - '01/2020'
            - '2020/01'
            - '20/01'
            - '01/20'
        - complete date
        - year
        - yime
        - date time
    - Phone Number
        - general phone number
        - special phone number ('*#')

    This transformation also translates the cases existed in test samples taken from:
    - [SemEval 2019 Task 10: Math Question Answering](https://www.aclweb.org/anthology/S19-2153.pdf)
    - [ChemistryQA](https://openreview.net/pdf?id=oeHTRAehiFF)
    - [PubmedQA](https://www.aclweb.org/anthology/D19-1259.pdf)
    - [SMD / KVRET](https://www.aclweb.org/anthology/2020.findings-emnlp.215/)
    - [Mathematics Dataset](https://openreview.net/pdf?id=H1gR5iR5FX)
    - [PubMed 200k RCT](https://www.aclweb.org/anthology/I17-2052.pdf)
    - [BBC News](https://www.kaggle.com/c/learn-ai-bbc)
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        perturbed = ""
        words = sentence.split()
        for i, word in enumerate(words):
            prev_word = (
                sentence.split()[i - 1] if i > 0 else " "
            )  # beginning of sentence
            next_word = (
                sentence.split()[i + 1]
                if i < len(sentence.split()) - 1
                else " "
            )  # end of sentence
            if perturbed != "":
                perturbed += " "
            perturbed += recognize_transform(word, prev_word, next_word)
        return [perturbed]


# if __name__ == '__main__':
#     import json
#     # from TestRunner import convert_to_snake_case
#     tf = NumericToWord()
#     sentence = "Please buy me 20 apples"
#     test_cases = []
#     for sentence in ["Please buy me 20 apples",
#                     "The deadline is in 2020/01/02",
#                     "The deadline is in 2020/01",
#                     "The deadline is in Jan 2020",
#                     "Slow down, it\'s still 5:00",
#                     "Quick!, it\'s already 23:00",
#                     "This is 2020!",
#                     "My phone number is +1371893178",
#                     "My phone number is +6287822216501",
#                     "My phone number is 6287822216501",
#                     "The price is $300",
#                     "The price is 300$",
#                     "The price is USD300",
#                     "The price is 300USD",
#                     "The price is USD300!@#!"]:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence}, "outputs": {"sentence": tf.generate(sentence)}}
#         )
#     json_file = {"type": "numeric_to_word", "test_cases": test_cases}
#     # json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json.dumps(json_file))

#     with open("test.json", "w") as out_file:
#         json.dump(json_file, out_file, indent=2, ensure_ascii=True)
