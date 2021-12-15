import random
import re
from abc import ABC

import nltk
import spacy
from nltk.corpus import stopwords, wordnet

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class InsertWordTransformation:
    nlp = None

    def __init__(self, seed=0, max_outputs=1, prob=0.5):
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.max_outputs = max_outputs
        self.seed = seed
        self.prob = prob
        self.stopwords = stopwords.words("english")

    def untokenize(self, words: list):
        """
        Untokenizing a text undoes the tokenizing operation, restoring
        punctuation and spaces to the places that people expect them to be.
        Ideally, `untokenize(tokenize(text))` should be identical to `text`,
        except for line breaks.
        ref: https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py#L28
        """
        text = " ".join(words)
        step1 = (
            text.replace("`` ", '"')
            .replace(" ''", '"')
            .replace(". . .", "...")
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

    def transform(self, input_text: str):
        random.seed(self.seed)
        pos_wordnet_dict = {
            "VERB": "v",
            "NOUN": "n",
            "ADV": "r",
            "ADJ": "s",
        }
        doc = self.nlp(input_text)
        results = set()
        for _ in range(self.max_outputs):
            result = []
            for token in doc:
                word = token.text
                wordnet_pos = pos_wordnet_dict.get(token.pos_)
                if not wordnet_pos:
                    result.append(word)
                elif word in self.stopwords:
                    result.append(word)
                else:
                    synsets = wordnet.synsets(word, pos=wordnet_pos)
                    if len(synsets) > 0:
                        synsets = [syn.name().split(".")[0] for syn in synsets]
                        synsets = [
                            syn
                            for syn in synsets
                            if syn.lower() != word.lower()
                        ]
                        synsets = list(
                            set(synsets)
                        )  # remove duplicate synonyms
                        if len(synsets) > 0 and random.random() < self.prob:
                            syn = random.choice(synsets)
                            syn = syn.replace("_", " ")
                            result.append(word)
                            result.append(syn)
                        else:
                            result.append(word)
                    else:
                        result.append(word)
            result = self.untokenize(result)  # rebuild the sentence
            results.add(result)
        return list(results)


"""
Insert words such as synonyms from WordNet via nltk.
"""


class SynonymInsertion(SentenceOperation, ABC):
    """
    This class is an implementation of synonym insertion in the sentence. Created by the Authors of TextAugment
    https://github.com/dsfsi/textaugment
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = False
    keywords = [
        "tokenizer",
        "external-knowledge-based",
        "lexical",
        "low-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        nltk.download(["wordnet", "stopwords"])
        self.insert_word_transformation = InsertWordTransformation(
            seed, max_outputs, prob
        )

    def generate(self, sentence: str):
        result = self.insert_word_transformation.transform(
            input_text=sentence,
        )
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return result
