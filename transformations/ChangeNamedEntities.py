from checklist.perturb import Perturb

from transformations.SentenceTransformation import SentenceTransformation
import spacy
"""
TODO: Would require changing on the side of the output too.
"""
class ChangeNamedEntities(SentenceTransformation):

    def __init__(self):
        # TODO: Do not repeat parse computations.
        self.nlp = spacy.load('en_core_web_sm')

    def generate(self, sentence: str):
        pertubed = Perturb.perturb([self.nlp(sentence)], Perturb.change_names, nsamples=1)
        pertubed = pertubed.data[0][1]
        print(f"Perturbed Input from {self.name()} : {pertubed}")