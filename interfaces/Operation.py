"""Generic operation class. """


class Operation(object):
    locales = None
    tasks = None
    seed = 0

    def __init__(self, seed=0, verbose=False):
        self.seed = seed
        self.verbose = verbose
        if self.verbose:
            print(f"Loading Operation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.locales

    @classmethod
    def name(cls):
        return cls.__name__
