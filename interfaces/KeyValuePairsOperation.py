from typing import Tuple, List

from interfaces.Operation import Operation


class KeyValuePairsOperation(Operation):
    """
    The base class for implementing transformations
     for inputs which take a structured form like AMR-to-text, E2E, etc.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
    "en_IN"
    """

    def generate(
        self, meaning_representation: dict, reference: str
    ) -> List[Tuple[dict, str]]:
        raise NotImplementedError

    def filter(self, meaning_representation: dict, reference: str) -> bool:
        raise True
