import itertools
import random
import re

import spacy
from nltk import download as nltkdl
from nltk import ne_chunk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tree import Tree

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def find_candidates(doc):
    """
    return the named entities, nouns and verbs as a list of candidates for hashtagify
    """
    chunked = ne_chunk(pos_tag(word_tokenize(doc.text)))
    candidates = []
    current_chunk = []
    for i in chunked:
        if type(i) == tuple:
            if i[1] in [
                "NN",
                "NNP",
                "NNPS",
                "VB",
                "VBD",
                "VBG",
                "VBN",
                "VBP",
                "VBZ",
            ]:
                if i[0] not in stopwords.words("english"):
                    candidates.append(i[0])

        if type(i) == Tree:
            current_chunk.append(
                " ".join([token for token, pos in i.leaves()])
            )

        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in candidates:
                candidates.append(named_entity)
                current_chunk = []
        else:
            continue
    return candidates


def hashtagify(sentence, nlp, prob=0.5, seed=666, max_outputs=1):
    """
    add hashtag prefix (#) to the candidates according to a fixed probability
    """
    random.seed(seed)
    doc = nlp(sentence)
    perturbed_texts = []

    for _ in itertools.repeat(None, max_outputs):
        # Generate the sentence with randomly placed hashtags
        transformed_sentence = sentence

        candidates = find_candidates(doc)
        for cand in candidates:
            if random.random() < prob:
                # Convert a word or multiple words to #word or #MultipleWords
                if len(cand.split()) == 1:
                    transformed_sentence = re.sub(
                        cand, "#" + cand, transformed_sentence
                    )
                else:
                    transformed_sentence = re.sub(
                        cand,
                        "#" + re.sub(" ", "", cand.title()),
                        transformed_sentence,
                    )

        perturbed_texts.append(transformed_sentence)

    return perturbed_texts


class HashtagifyTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "parser-based",
        "tokenizer-required",
        "chunker-required",
        "visual",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "social-reasoning",
    ]

    def __init__(self, seed=666, max_outputs=1):
        nltkdl("words")
        nltkdl("maxent_ne_chunker")
        nltkdl("punkt")
        nltkdl("averaged_perceptron_tagger")
        nltkdl("stopwords")
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = self.nlp = (
            spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        )

    def generate(self, sentence: str):
        perturbed_texts = hashtagify(
            sentence,
            self.nlp,
            prob=0.5,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
