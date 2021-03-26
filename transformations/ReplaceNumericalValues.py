from transformations.SentenceTransformation import SentenceTransformation
from common.NumericalTransformation import NumericalTransformation


class ReplaceNumericalValues(SentenceTransformation):

    numerical_transformation = None

    def __init__(self):
        self.numerical_transformation = NumericalTransformation()

    def generate(self, sentence: str):
        result = self.numerical_transformation.transform(sentence)

        print(f"Perturbed Input from {self.name()} : {result}")
        return result
