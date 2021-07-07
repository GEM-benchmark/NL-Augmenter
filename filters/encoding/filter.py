from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class TextEncodingFilter(SentenceOperation):
    tasks = [e for e in TaskType]
    languages = ["en", "de"]

    def __init__(self, encoding: str = "ascii"):
        super().__init__()
        self.encoding = encoding

    def filter(self, sentence: str = None) -> bool:
        contains_encoding = sentence != sentence.encode(self.encoding, "ignore").decode(self.encoding)
        return contains_encoding
