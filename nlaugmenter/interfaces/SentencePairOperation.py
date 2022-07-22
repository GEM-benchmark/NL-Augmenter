"""
Base Class for implementing the different input transformations or paraphrases.
"""
from typing import List, Tuple

from nlaugmenter.interfaces.Operation import Operation


class SentencePairOperation(Operation):
    """
    The base class for implementing augmentations/perturbations for sentence pair tasks like
    semantic similarity, entailment, etc.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
    "en_IN"
    """

    def generate(
        self, sentence1: str, sentence2: str, target: str
    ) -> List[Tuple[str, str, str]]:
        raise NotImplementedError

    def filter(self, sentence1: str, sentence2: str, target: str) -> bool:
        raise NotImplementedError
