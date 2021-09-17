from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp
import spacy


class TextContainsKeywordsFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords=None):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.punctuation = ['!', '.', '?', "'", '"', '(', ')', '-', ':', ';', ' ']

    def filter(self, sentence: str = None) -> bool:
        for c in sentence:
            if not c.isalnum() and c not in self.punctuation:
                return False
        return True
