from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class TextContainsNonAsciiFilter(SentenceOperation):
    tasks = [e for e in TaskType]
    languages = ["en", "de"]

    def filter(self, sentence: str = None) -> bool:
        contains_unicode = sentence != sentence.encode("ascii", "ignore").decode("ascii")
        return contains_unicode
