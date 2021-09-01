from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import unicodedata

class DiacriticRemoval(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):

        super().__init__()

    def strip_accents(self, sentence):

        sentence = unicodedata.normalize('NFD', sentence).encode('ascii', 'ignore').decode("utf-8")

        return str(sentence)

    def generate(self, sentence: str):

        return [self.strip_accents(sentence)]
