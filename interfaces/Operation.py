from typing import Tuple, List
from initialize import set_seed
"""Generic operation class. """


class Operation(object):
    languages = None
    tasks = None
    heavy = False
    max_outputs = 1

    def __init__(self, verbose=False, max_outputs=1):
        set_seed()
        self.verbose = verbose
        self.max_outputs = max_outputs
        if self.verbose:
            print(f"Loading Operation {self.name()}")
            
    @classmethod
    def compare(self, raw: object, pt: List[object]) -> Tuple[int, int]:
        successful_pt = 0
        failed_pt = 0
        for pt_example in pt:
            if pt_example == raw:
                failed_pt += 1
            else:
                successful_pt += 1
        return successful_pt, failed_pt

    @classmethod
    def is_heavy(cls):
        return cls.heavy

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages

    @classmethod
    def name(cls):
        return cls.__name__
