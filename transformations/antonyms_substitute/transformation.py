import re

import nltk
import spacy
from initialize import spacy_nlp
from nltk.corpus import wordnet
import numpy as np

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


"""
The code is adapted from @zijwang https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/synonym_substitution
"""


def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    ref: https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py#L28
    """
    text = " ".join(words)
    step1 = (
        text.replace("`` ", '"').replace(" ''", '"').replace(". . .", "...")
    )
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r" ([.,:;?!%]+)$", r"\1", step3)
    step5 = (
        step4.replace(" '", "'")
        .replace(" n't", "n't")
        .replace("can not", "cannot")
    )
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


def is_synonyms(word1, word2):
    synonyms = []
    for syn in wordnet.synsets(word1):
        for l in syn.lemmas():
            synonyms.append(l.name())
    if word2 in synonyms:
        return True
    return False

def is_antonyms(word1, word2):
    antonyms = []
    for syn in wordnet.synsets(word1):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    if word2 in antonyms:
        return True
    return False


def antonyms_substitute(text, spacy_pipeline, seed=22, max_outputs=1):
    np.random.seed(seed)
    upos_wn_dict = {
        # "VERB": "v",
        # "NOUN": "n",
        "ADV": "r",
        "ADJ": "s",
    }

    doc = spacy_pipeline(text)
    results = []
    for _ in range(max_outputs):
        result = []
        converted_words = []
        counter = 0
        for token in doc:
            word = token.text
            wn_pos = upos_wn_dict.get(token.pos_)
            if wn_pos is None:
                result.append(word)
            else:
                antonyms = []
                # synonyms = []
                for syn in wordnet.synsets(word, pos=wn_pos):
                    for l in syn.lemmas():
                        # synonyms.append(l.name())
                        if l.antonyms():
                            antonyms.append(l.antonyms()[0].name())
                antonyms = list(set(antonyms))

                if len(antonyms) > 0:
                    antonyms = sorted(antonyms)
                    result.append(antonyms[0].replace("_", " "))
                    counter += 1
                    converted_words.append(word)
                else:
                    result.append(word)

        # detokenize sentences
        result = untokenize(result)

        # choose even number of changes
        if counter%2 != 0:
            result = text

        # avoid doing transformation that original words are either synonyms or antonyms
        # e.g. do not transform "Ram is talented and skilled archer"
        for word1 in converted_words:
            for word2 in converted_words:
                if word1 != word2:
                    if is_antonyms(word1, word2) or is_synonyms(word1, word2):
                        result = text
                        break


        if result not in results:
            # make sure there is no dup in results
            results.append(result)
    return results


"""
Substitute words with antonyms using stanza (for POS) and wordnet via nltk (for antonyms)
"""


class AntonymsSubstitute(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = ["lexical", "noise", "rule-based", "tokenizer-required"]

    def __init__(self, seed=42, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.prob = prob
        nltk.download("wordnet")

    def generate(self, sentence: str):
        perturbed = antonyms_substitute(
            text=sentence,
            spacy_pipeline=self.nlp,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed
