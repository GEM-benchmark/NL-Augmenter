
"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class SentenceTransformation(object):

    def generate(self, sentence: str):
        pass

    def generateFromParse(self, parse):
        pass

    def name(self):
        return self.__class__.__name__
