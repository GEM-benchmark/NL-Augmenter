"""
Base Class for implementing the different challenge set transformations.
"""


class ChallengeSetTransformation(object):

    def generate(self, input: object):
        pass

    def name(self):
        return self.__class__.__name__
