
from interfaces.Operation import Operation

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

class SentencePairOperation(Operation):
    """
        The base class for implementing sentence pair level perturbations and transformations.

        "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
        given in tasks.TaskType.

        "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
        "en_IN"
        """

    def generate(self, sentence_1: str, sentence_2:str) -> tuple(str, str):
        raise NotImplementedError

    def filter(self, sentence_1: str, sentence_2:str) -> bool:
        raise NotImplementedError