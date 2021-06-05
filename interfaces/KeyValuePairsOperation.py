import abc
from typing import Tuple


class KeyValuePairsOperation(abc.ABC):
    """
     The base class for implementing transformations
      for inputs which take a structured form like AMR-to-text, E2E, etc.

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
    def generate(self, meaning_representation: dict, reference: str) -> Tuple[dict, str]:
        raise NotImplementedError

    def filter(self, meaning_representation: dict, reference: str) -> bool:
        raise NotImplementedError
