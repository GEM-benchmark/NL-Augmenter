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

     "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
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

     "src_locales", "tgt_locales :: The locales and/or languages for which this perturbation is applicable. eg. "es",
     "mr","en_IN"
    """

    src_locale = None
    tgt_locale = None
    tasks = None

    def __init__(self):
        super().__init__()
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.src_locale, cls.tgt_locale

    @classmethod
    def name(cls):
        return cls.__name__

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

     "src_locales", "tgt_locales :: The locales and/or languages for which this perturbation is applicable. eg. "es",
     "mr","en_IN"
    """

    src_locale = None
    tgt_locale = None
    tasks = None

    def __init__(self):
        super().__init__()
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.src_locale, cls.tgt_locale

    @classmethod
    def name(cls):
        return cls.__name__

    def generate(self, sentence: str, target: List[str]) -> Tuple[str, List[str]]:
        raise NotImplementedError

    def filter(self, sentence: str, target: List[str]) -> bool:
        raise NotImplementedError
