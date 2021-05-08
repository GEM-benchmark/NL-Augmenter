from checklist.perturb import Perturb

from interfaces.SentenceTransformation import SentenceTransformation
import spacy
from tasks.TaskTypes import TaskType


class WithoutPunctuation(SentenceTransformation):

    def __init__(self):
        tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
        locales = ["en"]
        super().__init__(tasks, locales)

        self.nlp = spacy.load('en_core_web_sm')

    def generate(self, sentence: str):
        pertubed = Perturb.strip_punctuation(self.nlp(sentence))
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed
