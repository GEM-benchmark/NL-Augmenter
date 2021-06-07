from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceOperation
import spacy
from tasks.TaskTypes import TaskType


class WithoutPunctuation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load('en_core_web_sm')

    def generate(self, sentence: str):
        pertubed = Perturb.strip_punctuation(self.nlp(sentence))
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed
