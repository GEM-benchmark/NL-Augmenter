import itertools
import json
import os
import random
import re

from nltk import download as nltkdl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def font_change(sentence, fonts, seed=666, max_outputs=1):
    """
    Randomly choose words and a font for each word and transform the characters one by one.

        parameters:
            sentence (str): input sentence
            fonts (dict): dictionary containing character replacements for various fonts
            max_outputs (int): number of outputs for each input

        returns:
            perturbed_texts (list): a list of sentences where random words are in different fonts.
    """
    random.seed(seed)
    perturbed_texts = []

    for _ in itertools.repeat(None, max_outputs):
        # tokens_match_list: a list of re.match objects of the words in the sentence. (No stop words)
        tokens_match_list = []
        for token in word_tokenize(sentence):
            if token not in stopwords.words("english"):
                if token != ".":
                    tokens_match_list.extend(
                        list(re.finditer(re.escape(token), sentence))
                    )

        transformed_sentence = list(sentence)

        # tokens_to_change: a list of randomly chosen words from tokens_match_list (up to three words)
        tokens_to_change = random.sample(
            tokens_match_list,
            random.randint(1, min(3, len(tokens_match_list) - 1)),
        )
        for ttc in tokens_to_change:
            while True:
                font = random.sample(list(fonts.keys()), 1)[0]
                if font != "normal":
                    break

            for i in range(ttc.start(), ttc.end()):
                try:
                    transformed_sentence[i] = fonts[font][
                        transformed_sentence[i]
                    ]
                except KeyError:
                    transformed_sentence[i] = transformed_sentence[i]

        perturbed_texts.append("".join(transformed_sentence))
    return perturbed_texts


class FontChange(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TAGGING,
    ]
    with open("list_of_languages.txt", "r") as f:
        languages = [x.rstrip() for x in f.readlines()]
    keywords = [
        "noise",
        "rule-based",
        "written",
        "visual",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "high-generations",
    ]

    def __init__(self, seed=664, max_outputs=1):
        nltkdl("stopwords")
        nltkdl("punkt")
        super().__init__(seed, max_outputs=max_outputs)

        # Mapping tables based on unicode-formatter (MIT license)
        # https://github.com/DenverCoder1/unicode-formatter

        dict_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fonts.json"
        )
        with open(dict_path) as f:
            self.fonts = json.load(f)

    def generate(self, sentence: str):
        perturbed_texts = font_change(
            sentence,
            self.fonts,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
