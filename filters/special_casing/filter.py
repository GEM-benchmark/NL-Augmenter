from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class TextSpecialCasingFilter(SentenceOperation):
    """Filter if any of the special casings appear in the sentence:
    All text is capitalized or All text is lowercased or there is Title Casing in the Sentence.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    def filter(self, sentence: str = None) -> bool:

        return any(
            [sentence.isupper(), sentence.islower(), sentence.istitle()]
        )
