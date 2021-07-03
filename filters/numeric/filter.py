from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from spacy import load


def has_number_in_digit(sentence):
    return any(char.isdigit() for char in sentence)


def has_number_in_words(tokens, numbers_in_words):
    for token in tokens:
        if token.text.lower() in numbers_in_words:
            word_flag = True
            return word_flag
        elif token.text[-2:] == "th":
            if token.text[:-2] in numbers_in_words:
                return True
    return False


class TextContainsNumberFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, has_digit=True, has_word=True):
        super().__init__()
        self.nlp = load("en_core_web_sm")
        self.has_digit = has_digit
        self.has_word = has_word
        self.numbers_in_words = ["one", "two", "three", "four", "five", "six", "seven", "eight",
                                 "nine", "ten","eleven", "twelve", "thirteen", "fourteen",
                                 "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
                                 "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
                                 "ninety", "hundred", "hundreds" "thousand", "thousands", "crore",
                                 "crores", "million", "millions", "billion", "billions", "first",
                                 "second", "third", "forth", "fifth", "eighth", "ninth"]

    def filter(self, sentence: str) -> bool:
        if self.has_digit:
            digit_flag = has_number_in_digit(sentence)
        if self.has_word:
            tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
            word_flag = has_number_in_words(tokenized, self.numbers_in_words)
        return digit_flag or word_flag


# if __name__ == "__main__":
#     import json
#     from TestRunner import convert_to_snake_case
#
#     ft = TextContainsNumberFilter(has_digit=True, has_word=True)
#     test_cases = []
#     inputs = ["I bought 5 mangoes from the market .",
#               "Where can I find some good online marketing courses .",
#               "John bought a car worth dollar twenty five thousand .",
#               "Khilji attacked India in eleventh century .",
#               "Taj mahal is the 7th wonder of the world ."
#               ]
#     for i, sentence in enumerate(inputs):
#         output = ft.filter(sentence)
#         test_cases.append({
#             "class": ft.name(),
#             "input": {"sentence": sentence},
#             "output": output,
#         })
#     json_file = {"type": convert_to_snake_case("numeric"), "test_cases": test_cases}
#     print(json.dumps(json_file))