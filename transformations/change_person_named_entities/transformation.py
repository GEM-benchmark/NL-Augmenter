import numpy as np
import spacy
from checklist.perturb import Perturb
from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ChangePersonNamedEntities(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "high-coverage", "high-precision"]

    def __init__(self, n=1, seed=0, max_outputs=2):
        # TODO: Do not repeat parse computations.
        super().__init__(seed, max_outputs=max_outputs)
        self.n = n
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        perturbed = Perturb.perturb(
            [self.nlp(sentence)], Perturb.change_names, nsamples=1
        )
        perturbed_texts = (
            perturbed.data[0][1 : self.max_outputs]
            if len(perturbed.data) > 0
            else [sentence]
        )
        return perturbed_texts
