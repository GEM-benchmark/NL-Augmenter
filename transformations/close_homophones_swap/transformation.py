import random

import spacy
from SoundsLike.SoundsLike import Search

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def close_homophones_swap(text, corrupt_prob, seed=0, max_outputs=1, nlp=None):
    random.seed(seed)
    doc = nlp(text)
    perturbed_texts = []
    spaces = [True if tok.whitespace_ else False for tok in doc]
    for _ in range(max_outputs):
        perturbed_text = []
        for index, token in enumerate(doc):
            if random.uniform(0, 1) < corrupt_prob:
                try:
                    replacement = random.choice(
                        Search.closeHomophones(token.text)
                    )
                    if (
                        replacement.lower() != token.text.lower()
                        and token.text.lower() != "a"
                    ):
                        perturbed_text.append(replacement)
                    else:
                        perturbed_text.append(token.text)
                except Exception:
                    perturbed_text.append(token.text)
            else:
                perturbed_text.append(token.text)

        textbf = []
        for index, token in enumerate(perturbed_text):
            textbf.append(token)
            if spaces[index]:
                textbf.append(" ")
        perturbed_texts.append("".join(textbf))
    return perturbed_texts


class CloseHomophonesSwap(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "high-coverage",
        "high-precision",
        "unnaturally-written",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed)
        self.max_outputs = max_outputs
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        perturbed_texts = close_homophones_swap(
            text=sentence,
            corrupt_prob=0.5,
            seed=self.seed,
            max_outputs=self.max_outputs,
            nlp=self.nlp,
        )
        return perturbed_texts
