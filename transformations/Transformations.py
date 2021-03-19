from transformations.BackTranslation import BackTranslation
from transformations.ButterFingersPerturbation import ButterFingersPerturbation
from transformations.ChangeNamedEntities import ChangeNamedEntities
from transformations.SentenceTransformation import SentenceTransformation
from transformations.SpeechConversionError import SpeechConversionError
from transformations.WithoutPunctuation import WithoutPunctuation
#from transformations.CorefSwap import CorefSwap
from transformations.ReplaceNumericalValues import ReplaceNumericalValues
#from transformations.CorefSwap import CorefSwap


class TransformationsList(SentenceTransformation):

    def __init__(self):
        transformations = []
        transformations.append(ReplaceNumericalValues())
        transformations.append(ButterFingersPerturbation())
        transformations.append(WithoutPunctuation())
        transformations.append(ChangeNamedEntities())
        transformations.append(BackTranslation())
        #transformations.append(CorefSwap()) TODO: @Varun
        transformations.append(SpeechConversionError())
        self.transformations = transformations

    def generate(self, sentence: str):
        print(f"Original Input : {sentence}")
        generations = {"Original": sentence}
        for transformation in self.transformations:
            generations[transformation.name()] = transformation.generate(sentence)
        return generations
