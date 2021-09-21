import random
import re
import string

import pronouncing
import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def grapheme_phoneme(grapheme):
    """
    converts each word to phonems. If there are multiple pronounciation of a
    word, only the first prononciation is taken. Stress information from each
    word is removed.
    """
    phoenems = pronouncing.phones_for_word(grapheme)

    if len(phoenems) > 0:
        phoenem_without_stress = "".join(
            [x for x in phoenems[0] if x.isalpha()]
        ).lower()
        transformed_word = phoenem_without_stress
    else:
        transformed_word = grapheme

    return transformed_word


def phoneme_substitution(
    text, spacy_pipeline, prob=0.5, seed=0, max_outputs=1
):
    random.seed(seed)

    """
    returns transformed sentence with words replaced with their pronunciation
    based on probability.
    """

    doc = spacy_pipeline(text)

    transformed_words = []
    for token in doc:
        word = token.text
        if word in string.punctuation:
            transformed_words[-1] += word
        else:

            if random.random() < prob:
                new_word = grapheme_phoneme(word)
                transformed_words.append(new_word)
            else:
                transformed_words.append(word)

    transformed_sentence = [" ".join(transformed_words)]

    return [transformed_sentence]


class PhonemeSubstitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = ["lexical", "noise", "noise", "api-based", "aural", "high-precision"]

    def __init__(self, seed=0, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.spacy_pipeline = (
            spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        )
        self.prob = prob

    def generate(self, sentence: str):
        perturbed = phoneme_substitution(
            text=sentence,
            spacy_pipeline=self.spacy_pipeline,
            seed=self.seed,
            prob=self.prob,
            max_outputs=self.max_outputs,
        )
        return perturbed
