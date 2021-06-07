from interfaces.Operation import Operation

"""
Base class for implementing contrast set transformation on a given input dataset.
"""


class ContrastSetOperation(Operation):
    """
    The base class for implementing dataset level contrast set formations from a given dataset.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
    "en_IN"
    """

    locales = None
    tasks = None

    @classmethod
    def domain(cls):
        return cls.tasks, cls.locales

    @classmethod
    def name(cls):
        return cls.__name__

    def generate(self, dataset: dict, field_name: str) -> dict:
        raise NotImplementedError
