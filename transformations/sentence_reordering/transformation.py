import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import nltk

nltk.download("punkt")  # required for sent_tokenize
from nltk.tokenize import sent_tokenize
import random

import spacy

nlp = spacy.load("en_core_web_sm")

# Add neural coref to SpaCy's pipe
import neuralcoref

neuralcoref.add_to_pipe(nlp)


"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def sentence_reordering(text, seed):
    random.seed(seed)
    # resolve coref
    text = nlp(text)._.coref_resolved

    # tokenize and shuffle
    text_split = sent_tokenize(text)
    random.shuffle(text_split)
    return " ".join(text_split)


"""
Shuffle sentence order
"""


class SentenceReordering(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, max_output=1):
        super().__init__(seed)
        self.max_output = max_output

    def generate(self, sentence: str):
        pertubed = [sentence_reordering(text=sentence, seed=self.seed)]
        return pertubed
