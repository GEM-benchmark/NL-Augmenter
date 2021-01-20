from checklist.perturb import Perturb

from transformations.SentenceTransformation import SentenceTransformation
import spacy

class WithoutPunctuation(SentenceTransformation):

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def generate(self, sentence: str):
        pertubed = Perturb.strip_punctuation(self.nlp(sentence))
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed