import inflect

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

"""
Verbalizing numbers of the text
"""


infEng = inflect.engine()


def word_to_number(text):
    results = []
    trans = []
    for token in text.split():
        if token.isdigit():
            words = infEng.number_to_words(int(token), wantlist=True)
            trans.extend(words)
        else:
            trans.append(token)
    results.append(" ".join(trans))
    return results


class NumberToWord(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    locales = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = word_to_number(text=sentence)
        return pertubed
