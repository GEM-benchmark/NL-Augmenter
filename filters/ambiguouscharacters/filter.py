from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class AmbiguousCharactersFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords=None):
        super().__init__()
        self.ambiguous_chars = [
                                '0', 'O', 'D', 'o', 'Q',
                                'l', '1', 'I', 'i', '!', '|',
                                'B', '8',
                                'Z', '2',
                                'S', '5',
                                'G', '6',
                                "'", '`',
                                ]

    def filter(self, sentence: str = None) -> bool:
        for c in sentence:
            if c in self.ambiguous_chars:
                return False
        return True
