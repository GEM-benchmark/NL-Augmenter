from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from text2nums import *


class WordsToNumbers(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "written", "highly-meaning-preserving", "high-precision", "low-generations"]

    def __init__(self, seed: int = 0) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        return [text2int(sentence)]
