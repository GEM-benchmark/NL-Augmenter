import abc
from typing import Tuple, List


class QuestionAnswerTransformation(object):
    """
     The base class for implementing question answering style perturbations and transformations.

     "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
     given in tasks.TaskType.

     "locales" :: The locales and/or languages for which these perturbation are applicable. eg. "es",
     "mr","en_IN". If the context, question and answer are in separate locales, the implementation can
     accordingly override the domain(cls) function.
    """

    locales = None
    tasks = None

    def __init__(self):
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.locales, cls.locales, cls.locales

    @classmethod
    def name(cls):
        return cls.__name__

    @abc.abstractmethod
    def generate(self, context: str, question: str, answer: [str]) -> Tuple[str, str, List[str]]:
        raise NotImplementedError
