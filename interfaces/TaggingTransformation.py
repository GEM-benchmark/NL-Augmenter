import abc
from typing import Tuple, List

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class TaggingTransformation(abc.ABC):
    """
     The base class for implementing tagging ({word_i,tag_i}* --> {word_j,tag_j}*) perturbations and transformations.

     "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
     given in tasks.TaskType.

     "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
     "en_IN"
    """

    locales = None
    tasks = None

    def __init__(self):
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.locales

    @classmethod
    def name(cls):
        return cls.__name__

    @abc.abstractmethod
    def generate(self, token_sequence: List[str], tag_sequence: List[str]) -> Tuple[List[str], List[str]]:
        raise NotImplementedError

    def generateFromParse(self, parse, tag_sequence: List[str]) -> Tuple[str, List[str]]:
        raise NotImplementedError
