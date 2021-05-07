from transformations.SentenceTransformation import SentenceTransformation
from common.NumericalTransformation import NumericalTransformation
from tasks.TaskTypes import TaskType


class ReplaceNumericalValues(SentenceTransformation):
    numerical_transformation = None

    def __init__(self):
        tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
        locales = ["en"]
        super().__init__(tasks, locales)

        self.numerical_transformation = NumericalTransformation()

    def generate(self, sentence: str):
        result = self.numerical_transformation.transform(sentence)

        print(f"Perturbed Input from {self.name()} : {result}")
        return result
