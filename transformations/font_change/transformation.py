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

nltkdl("stopwords")
nltkdl("punkt")


# import spacy

# from nltk import ne_chunk
# from nltk.tag import pos_tag
# from nltk.tree import Tree

# nltkdl("words")
# nltkdl("maxent_ne_chunker")

# nltkdl("averaged_perceptron_tagger")


# def find_candidates(doc):
#     chunked = ne_chunk(pos_tag(word_tokenize(doc.text)))
#     candidates = []
#     current_chunk = []
#     for i in chunked:
#         if type(i) == tuple:
#             if i[1] in [
#                 "NN",
#                 "NNP",
#                 "NNPS",
#                 "VB",
#                 "VBD",
#                 "VBG",
#                 "VBN",
#                 "VBP",
#                 "VBZ",
#             ]:
#                 if i[0] not in stopwords.words("english"):
#                     candidates.append(i[0])
#
#         if type(i) == Tree:
#             current_chunk.append(
#                 " ".join([token for token, pos in i.leaves()])
#             )
#
#         if current_chunk:
#             named_entity = " ".join(current_chunk)
#             if named_entity not in candidates:
#                 candidates.append(named_entity)
#                 current_chunk = []
#         else:
#             continue
#     return candidates


def font_change(sentence, fonts, seed=666, max_outputs=1):
    random.seed(seed)
    perturbed_texts = []

    for _ in itertools.repeat(None, max_outputs):
        # Generate the sentence with randomly distributed fonts
        tokens_escaped_list = []
        for token in word_tokenize(sentence):
            if token not in stopwords.words("english"):
                if token != ".":
                    tokens_escaped_list.extend(
                        list(re.finditer(re.escape(token), sentence))
                    )

        transformed_sentence = list(sentence)

        tokens_to_change = random.sample(
            tokens_escaped_list,
            random.randint(1, min(3, len(tokens_escaped_list) - 1)),
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


class Font_Change(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION]
    languages = ["en"]

    def __init__(self, seed=664, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
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
