from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceOperation
import spacy
from tasks.TaskTypes import TaskType


class Punctuation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        pertubed = Perturb.punctuation(self.nlp(sentence))
        pertubed = pertubed[0]  # Just take the first one for now.
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed
