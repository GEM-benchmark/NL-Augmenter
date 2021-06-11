import numpy as np

from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceOperation
import spacy
from tasks.TaskTypes import TaskType


class ChangePersonNamedEntities(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self, n=1, seed=0):
        # TODO: Do not repeat parse computations.
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        pertubed = Perturb.perturb(
            [self.nlp(sentence)], Perturb.change_names, nsamples=1
        )
        pertubed = pertubed.data[0][1] if len(pertubed.data) > 0 else sentence
        return pertubed
