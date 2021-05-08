"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class SentenceTransformation(object):
    """
     The base class for implementing sentence-level perturbations and transformations.

     "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
     given in tasks.TaskType.

     "locales" :: The locales and/or languages for which this perturbation is applicable. eg. "es", "mr",
     "en_IN"
    """

    def __init__(self, tasks: list, locales: list):
        self.tasks = tasks
        self.locales = locales

    def generate(self, sentence: str):
        pass

    def generateFromParse(self, parse):
        pass

    def name(self):
        return self.__class__.__name__


class SentenceAndTargetTransformation(object):
    """
     The base class for implementing sentence-pair-level perturbations and transformations .

     "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
     given in tasks.TaskType.

     "src_locales", "tgt_locales :: The locales and/or languages for which this perturbation is applicable. eg. "es",
     "mr","en_IN"
    """

    def __init__(self, tasks: list, src_locales: list, tgt_locales: list):
        self.tasks = tasks
        self.src_locales = src_locales
        self.tgt_locales = tgt_locales

    def generate(self, sentence: str, target: str):
        pass

    def generateFromParse(self, parse, target: str):
        pass

    def name(self):
        return self.__class__.__name__
