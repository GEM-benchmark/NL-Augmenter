import random
import re
from abc import ABC

import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class SwapWordTransformation:
    nlp = None

    def __init__(self, seed=0, max_outputs=1, prob=0.5):
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.max_outputs = max_outputs
        self.seed = seed
        self.prob = prob

    @staticmethod
    def untokenize(words: list):
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

    def transform(self, input_text: str):
        random.seed(self.seed)
        doc = self.nlp(input_text)
        results = list()
        for _ in range(self.max_outputs):
            doc_list = [i.text for i in doc]
            doc_idx = []
            for _, i in enumerate(doc):
                if i.pos_ != 'PUNCT':
                    doc_idx.append(_)

            random_start_idx = random.randint(0, len(doc_idx) - 1)
            swap_direction = [-1, 1]
            if len(doc_idx) in [0, 1]:
                results.append(doc.text)
                continue
            if random_start_idx == 0:
                swap_word_idx = random_start_idx+swap_direction[1]
            elif random_start_idx == len(doc_idx):
                swap_word_idx = random_start_idx+swap_direction[0]
            else:
                swap_word_idx = random_start_idx + random.choice(swap_direction)

            random_start = doc_idx[random_start_idx]
            swap_word_idx = doc_idx[swap_word_idx]

            random_start_word = doc[random_start].text
            swap_word = doc[swap_word_idx].text

            doc_list[random_start] = swap_word
            doc_list[swap_word_idx] = random_start_word
            result = self.untokenize(doc_list)
            results.append(result)
        return results


"""
Randomly swap words that are close to each other.
"""


class RandomSwap(SentenceOperation, ABC):
    """
    This class is an implementation of random swapping of words in a sentence. Created by the Authors of TextAugment
    https://github.com/dsfsi/textaugment
    """
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.swap_word_transformation = SwapWordTransformation(
            seed, max_outputs, prob
        )

    def generate(self, sentence: str):
        result = self.swap_word_transformation.transform(
            input_text=sentence,
        )
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return result
