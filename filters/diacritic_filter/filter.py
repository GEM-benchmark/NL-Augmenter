import unicodedata

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class DiacriticFilter(SentenceOperation):
    """
    Filter if the input sentence has any diacritic marks.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "en",
        "fr",
        "es",
        "it",
        "pt",
        "fi",
        "nl",
        "da",
        "cs",
        "hr",
        "bg",
        "be",
        "eu",
        "ru",
        "uk",
        "pl",
        "sv",
        "sk",
        "sl",
    ]
    keywords = [
        "visual",
        "morphological",
        "rule-based",
        "written",
        "highly-meaning-preserving",
        "high-precision",
    ]

    def __init__(self):
        super().__init__()

    @staticmethod
    def strip_accents(sentence):

        return str(
            unicodedata.normalize("NFD", sentence)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )

    def filter(self, sentence: str = None) -> bool:
        return sentence != self.strip_accents(sentence)
