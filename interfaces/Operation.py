"""Generic operation class. """


class Operation(object):
    languages = None
    tasks = None
    seed = 0
    heavy = False
    max_output = 1

    def __init__(self, seed=0, verbose=False, max_output=1):
        self.seed = seed
        self.verbose = verbose
        self.max_output = max_output
        if self.verbose:
            print(f"Loading Operation {self.name()}")

    @classmethod
    def is_heavy(cls):
        return cls.heavy

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages

    @classmethod
    def name(cls):
        return cls.__name__
