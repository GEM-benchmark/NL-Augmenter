from tasks.TaskTypes import TaskType

class AlphanumericFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords=None):
        super().__init__()
        self.punctuation = ['!', '.', '?', "'", '"', '(', ')', '-', ':', ';', ' ']

    def filter(self, sentence: str = None) -> bool:
        for c in sentence:
            if not c.isalnum() and c not in self.punctuation:
                return False
        return True
