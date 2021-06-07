class Operation(object):
    locales = None
    tasks = None

    def __init__(self):
        print(f"Loading Operation {self.name()}")

    @classmethod
    def domain(cls):
        return cls.tasks, cls.locales

    @classmethod
    def name(cls):
        return cls.__name__
