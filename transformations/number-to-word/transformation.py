import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import inflect

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


infEng = inflect.engine()

def word_to_number(text):

    trans = []
    for token in text.split():
        if token.isdigit():
            words = infEng.number_to_words(int(token), wantlist=True)      
            trans.extend(words)
        else:
            trans.append(token)


    return ' '.join(trans)




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


