from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from .text2nums import *


class WordsToNumbers(SentenceOperation):
    '''
    Transforms a given sentence that has "word numbers" to their numerical representations, e.g.
    "I have ten cats" -> "I have 10 cats."

    Inherits from SentenceOperation.
    '''
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.PARAPHRASE_DETECTION, TaskType.TEXTUAL_ENTAILMENT]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "written", "highly-meaning-preserving", "high-precision", "low-generations"]

    def __init__(self, seed: int = 0, max_outputs=1) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        return [text2int(sentence)]
