from tasks.TaskTypes import TaskType
from interfaces.SentenceOperation import SentenceOperation

class AlphanumericFilter(SentenceOperation):
    """
    Filters sentence that characters which are a) not alphanumeric and b) not common punctuation.

    Inherits SentenceOperation.
    """
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["highly-meaning-preserving", "low-generations", "rule-based"]

    def __init__(self):
        super().__init__()
        self.punctuation = ['!', '.', '?', "'", '"', '(', ')', '-', ':', ';', ' ']

    def filter(self, sentence: str = None) -> bool:
        for c in sentence:
            if not c.isalnum() and c not in self.punctuation:
                return False
        return True
