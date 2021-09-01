from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import unicodedata

class DiacriticFilter(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    def strip_accents(self, sentence):

        return str(unicodedata.normalize('NFD', sentence).encode('ascii', 'ignore').decode("utf-8"))

    def filter(self, sentence: str = None) -> bool:

        return sentence != self.strip_accents(sentence)
