from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from spacy import load

"""
A filter on the sentence contains negated words.
"""


class NegationFilter(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION,
             TaskType.SENTIMENT_ANALYSIS,]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = load('en_core_web_sm')
        self.negative_words = ["not", "n't", "never", "nt"]

    def filter(self, sentence: str) -> bool:
        doc = self.nlp(sentence, disable=["parser", "ner"])
        for token in doc:
            if token.text.lower() in self.negative_words:
                return True
        return False


# if __name__ == "__main__":
#     import json
#     from TestRunner import convert_to_snake_case
#
#     ft = NegationFilter()
#     test_cases = []
#     inputs = ["I didn't like pizza.",
#               "We shouldnt become a part of troll army on internet.",
#               "Anil Kumble is the highest wicket taker from India.",
#               "RNN can't resolve long terms dependency problems effectively.",
#               "John never want to open a bank account."]
#     for i, sentence in enumerate(inputs):
#         output = ft.filter(sentence)
#         test_cases.append({
#             "class": ft.name(),
#             "inputs": {"sentence":sentence},
#             "outputs": output,
#         })
#     json_file = {"type":convert_to_snake_case("negation"), "test_cases":test_cases}
#     print(json.dumps(json_file))
