from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class TextContainsNonAsciiFilter(SentenceOperation):
    tasks = [e for e in TaskType]
    languages = ["en", "de", "all"]

    def __init__(self):
        super().__init__()

    def filter(self, sentence: str = None) -> bool:
        print(sentence)
        contains_unicode = sentence != sentence.encode("ascii", "ignore").decode("ascii")
        return contains_unicode
