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


class SentenceAndLabelTransformation(object):

    def generate(self, sentence: str, label: str):
        pass

    def generateFromParse(self, parse, label: str):
        pass

    def name(self):
        return self.__class__.__name__
