import random
import numpy as np

from checklist.perturb import Perturb

from interfaces.SentenceTransformation import SentenceTransformation
import spacy
from tasks.TaskTypes import TaskType


class ChangeNamedEntities(SentenceTransformation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self, n=1):
        # TODO: Do not repeat parse computations.
        super().__init__()
        random.seed(0)
        self.nlp = spacy.load('en_core_web_sm')
        self.n = n

    def generate(self, sentence: str):
        np.random.seed(0)
        pertubed = Perturb.perturb([self.nlp(sentence)], Perturb.change_names, nsamples=1)
        pertubed = pertubed.data[0][1] if len(pertubed.data) > 0 else sentence
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed
