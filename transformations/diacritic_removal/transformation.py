from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import unicodedata

class DiacriticRemoval(SentenceOperation):
    """
    Transforms an input sentence by removing any diacritic marks.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr", "es", "it", "pt", "fi", "nl", "da", "cs", "hr", "bg", "be", "eu", "ru", "uk", "pl", "sv", "sk", "sl"]
    keywords = ["diacritic", "language-agnostic"]

    def __init__(self):

        super().__init__()

    def strip_accents(self, sentence):

        sentence = unicodedata.normalize('NFD', sentence).encode('ascii', 'ignore').decode("utf-8")

        return str(sentence)

    def generate(self, sentence: str):

        return [self.strip_accents(sentence)]
