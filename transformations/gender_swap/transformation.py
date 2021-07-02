from typing import Dict, List, Sequence

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
TODO desc
"""

class GenderSwap(SentenceOperation):
    tasks = [ # TODO verify it
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    _gender_pairs_path = "gender_pairs.csv"

    def __init__(self) -> None:
        super().__init__()

    def _get_pairs(self) -> Dict[str, str]:
        """Reads csv file and retruns dict of gender pairs."""
        with open(self._gender_pairs_path) as f:
            pairs = [l.strip('\n').split(',') for l in f.readlines()]

        male2female = {p[0]: p[1] for p in pairs}
        female2male = {p[1]: p[0] for p in pairs}

        return {**male2female, **female2male}

    def generate(self, sentence: str) -> List[str]:
        return sentence


if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    gs = GenderSwap()
    y = gs._get_pairs()

    print(y)