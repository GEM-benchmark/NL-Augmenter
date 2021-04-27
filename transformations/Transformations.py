
from transformations.BackTranslation import BackTranslation
from transformations.ButterFingersPerturbation import ButterFingersPerturbation
from transformations.ChangeNamedEntities import ChangeNamedEntities
from transformations.SentenceTransformation import SentenceTransformation
from transformations.WithoutPunctuation import WithoutPunctuation


class TransformationsList(SentenceTransformation):

    def __init__(self):
        transformations = [ButterFingersPerturbation(), WithoutPunctuation(), ChangeNamedEntities(), BackTranslation()]
        self.transformations = transformations

    def generate(self, sentence: str):
        print(f"Original Input : {sentence}")
        generations = {"Original": sentence}
        for transformation in self.transformations:
            generations[transformation.name()] = transformation.generate(sentence)
        return generations
