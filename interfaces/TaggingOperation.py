from typing import Tuple, List

from interfaces.Operation import Operation

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class TaggingOperation(Operation):
    """
     The base class for implementing tagging ({word_i,tag_i}* --> {word_j,tag_j}*) perturbations and transformations.

     "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
     given in tasks.TaskType.

     "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
     "en_IN"
    """

    def generate(self, token_sequence: List[str], tag_sequence: List[str]) -> Tuple[List[str], List[str]]:
        raise NotImplementedError

    def filter(self, token_sequence: List[str], tag_sequence: List[str]) -> bool:
        raise NotImplementedError
