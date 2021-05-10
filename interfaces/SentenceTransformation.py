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

    def generate(self, sentence: str):
        pass

    def generateFromParse(self, parse):
        pass


class SentenceAndTargetTransformation(object):
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
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.src_locale, cls.tgt_locale

    @classmethod
    def name(cls):
        return cls.__name__

    def generate(self, sentence: str, target: str):
        pass

    def generateFromParse(self, parse, target: str):
        pass


class SentenceAndTargetsTransformation(object):
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
        print(f"Loading Transformation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.src_locale, cls.tgt_locale

    @classmethod
    def name(cls):
        return cls.__name__

    def generate(self, sentence: str, target: [str]):
        pass

    def generateFromParse(self, parse, target: [str]):
        pass
