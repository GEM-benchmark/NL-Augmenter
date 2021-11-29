from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class AmbiguousCharactersFilter(SentenceOperation):
    """
    Filters sentence that contain ambiguous characters. The characters that might be ambiguous are defined below.

    Inherits SentenceOperation.
    """
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["highly-meaning-preserving", "low-generations", "rule-based"]

    def __init__(self):
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
