import itertools
import random
import spacy
import numpy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from SoundsLike.SoundsLike import Search
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def close_homophones_swap(text, corrupt_prob, seed=0, max_output=1):
    random.seed(seed)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    perturbed_texts = []
    spaces = [True if tok.whitespace_ else False for tok in doc]
    for _ in range(max_output):
        perturbed_text = []
        for index, token in enumerate(doc):
            if random.uniform(0, 1) < corrupt_prob:
                try:
                    replacement = random.choice(Search.closeHomophones(token.text))
                    perturbed_text.append(replacement)
                except:
                    perturbed_text.append(token.text)
            else:
                perturbed_text.append(token.text)
        
        textbf = []             
        for index, token in enumerate(perturbed_text):
            textbf.append(token)
            if spaces[index]:
                textbf.append(' ')
        perturbed_texts.append(''.join(textbf))
    return perturbed_texts
       
class CloseHomophonesSwap(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        self.max_output = max_output

    def generate(self, sentence: str):
        perturbed_texts = close_homophones_swap(
            text=sentence, corrupt_prob=0.5, seed=self.seed, max_output=self.max_output
        )
        return perturbed_texts
