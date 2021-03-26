"""
Base Class for implementing the different data transformations a generation should be robust against.
"""


class DataTransformation(object):

    def generate(self, input: object, data_subset: str, dataset_size=None):
        pass

    def name(self):
        return self.__class__.__name__
