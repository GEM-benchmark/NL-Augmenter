import spacy
import json
import os
from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class CorrectCommonMisspellings(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "external-knowledge-based",
        "tokenizer-required",
        "highly-meaning-preserving",
        "high-coverage",
        "low-generations",
    ]

    def __init__(self):
        super().__init__()
        self.COMMON_MISSPELLINGS_DICT = get_common_misspellings_dict()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        doc = self.nlp(sentence)
        perturbed_text = [
            self.COMMON_MISSPELLINGS_DICT.get(token.text, token.text) + " "
            if token.whitespace_
            else self.COMMON_MISSPELLINGS_DICT.get(token.text, token.text)
            for token in doc
        ]
        return ["".join(perturbed_text)]


def get_common_misspellings_dict():
    spell_corrections = os.path.join(
        "transformations", "replace_spelling", "spell_corrections.json"
    )
    with open(spell_corrections, "r") as fp:
        spell_corrections = json.load(fp)
    return spell_corrections


"""
# code to process machine-readable text into this list (first save from wikipedia into dict.txt)
import numpy as np

# read everything in
d = np.loadtxt("dict.txt", delimiter="->", dtype=str)

# prune anything with commas
unique_idxs = np.array([len(x.split()) == 1 for x in d[:, 1]])
d = d[unique_idxs]

# print as dict
d = {d[i, 0]: d[i, 1] for i in range(d.shape[0])}
print(d)
"""
