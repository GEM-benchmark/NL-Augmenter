import json
import os

import spacy

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.utils.initialize import spacy_nlp


class DyslexiaWordsSwap(SentenceOperation):
    """Altering some words with mistakes that are likely to happen in the context of dyslexia.

    Args:
        seed: initial seed. Defaults: 0.
        max_outputs: maximum number of generated outputs. Defaults: 1.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "aural",
        "possible-meaning-alteration",
        "low-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed=seed, max_outputs=max_outputs)

        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        with open(
            os.path.join(os.path.dirname(__file__), "data.json"), "r"
        ) as infile:
            data = json.load(infile)
        self.swap_words = {
            k: v for dict in data.values() for k, v in dict.items()
        }
        self.swap_words_2 = {v: k for k, v in self.swap_words.items()}

    def generate(self, sentence: str):
        end_idx = 0
        new_sentence = ""
        for word in self.nlp(sentence):
            new_sentence += sentence[end_idx : word.idx]

            new_word = word.text
            key = word.text.lower()
            if key in self.swap_words or key in self.swap_words_2:
                if key in self.swap_words:
                    new_word = self.swap_words[key]
                if key in self.swap_words_2:
                    new_word = self.swap_words_2[key]
            new_sentence += new_word

            end_idx = word.idx + len(word.text)
        new_sentence += sentence[end_idx:]

        return [new_sentence]
