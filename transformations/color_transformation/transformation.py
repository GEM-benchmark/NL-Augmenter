import json
import os
import random

import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def get_(big_list, small_list):
    big_str = " ".join(big_list)
    small_str = " ".join(small_list)

    big_str.index(small_str)


"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class ColorTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "tokenizer-required",
        "unnatural-sounding",
        "unnaturally-written",
        "possible-meaning-alteration",
        "high-precision",
        "low-coverage",
        "high-generations",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.load_color_names()
        self.detokenizer = TreebankWordDetokenizer()

    def load_color_names(self):
        filepath = os.path.realpath(
            os.path.join(
                os.getcwd(), os.path.dirname(__file__), "colors.json"
            )
        )

        with open(filepath, "r") as f:
            self.colors = json.load(f)
        self.color_names = [color["name"] for color in self.colors.values()]

    def generate(self, sentence: str, mapping: dict = None):
        """
        Tranform input sentence using a given mapping.

        User can customize transformations by providing a mapping dictionary.
        This dictionary has colors as keys and transformable colors as values.
        If a color is missing from the keys, any color is used for transformation.
        """
        if mapping is None: mapping = {}

        random.seed(self.seed)

        # Detokenize sentence
        try:
            words = nltk.word_tokenize(sentence)
        except LookupError:
            nltk.download("punkt")
            words = nltk.word_tokenize(sentence)
        sentence = self.detokenizer.detokenize(words)

        # Detect colors in a given sentence
        colors_and_indices = []
        for color_name in self.color_names:
            try:
                idx = sentence.index(color_name)
            except ValueError:
                continue
            colors_and_indices.append((color_name, idx, idx + len(color_name)))

        # Transform colors
        new_sentences = []
        for _ in range(self.max_outputs):
            new_sentence = sentence
            for color, start_idx, end_idx in colors_and_indices[::-1]:
                # Choose color
                if color not in mapping:
                    new_color = random.choice(self.color_names)
                else:
                    new_color = random.choice(mapping[new_color])
                # Generate sentence
                new_sentence = (
                    new_sentence[:start_idx]
                    + new_color
                    + new_sentence[end_idx:]
                )
            new_sentences.append(new_sentence)

        return new_sentences
