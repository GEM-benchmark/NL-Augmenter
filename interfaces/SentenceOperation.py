from typing import Tuple, List

from interfaces.Operation import Operation

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class SentenceOperation(Operation):
    """
    The base class for implementing sentence-level perturbations and transformations.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
    "en_IN"
    """

    def generate(self, sentence: str) -> str:
        raise NotImplementedError

    def filter(self, sentence: str) -> bool:
        raise NotImplementedError


class SentenceAndTargetOperation(Operation):
    """
    The base class for implementing sentence-pair-level perturbations and transformations. The target could be
    either a class label (eg. sentiment analysis) or a target utterance (eg. machine translation).

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages", "tgt_languages :: The locales and/or languages for which this perturbation is applicable. eg. "es",
    "mr","en_IN"
    """

    languages = None
    tgt_languages = None
    tasks = None

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages, cls.tgt_languages

    def generate(self, sentence: str, target: str) -> Tuple[str, str]:
        raise NotImplementedError

    def filter(self, sentence: str, target: str) -> bool:
        raise NotImplementedError


class SentenceAndTargetsOperation(Operation):
    """
    The base class for implementing sentence-pair-level perturbations and transformations. There can be
    muliple targets eg. multiple references in machine translation.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages", "tgt_languages :: The locales and/or languages for which this perturbation is applicable. eg. "es",
    "mr","en_IN"
    """

    languages = None
    tgt_languages = None
    tasks = None

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages, cls.tgt_languages

    def generate(self, sentence: str, target: List[str]) -> Tuple[str, List[str]]:
        raise NotImplementedError

    def filter(self, sentence: str, target: List[str]) -> bool:
        raise NotImplementedError
