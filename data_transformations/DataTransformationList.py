from data_transformations.DataTransformation import DataTransformation
from data_transformations.ReplaceDataNumericalValues import ReplaceDataNumericalValues

class DataTransformationList(DataTransformation):

    def __init__(self):
        transformations = []
        transformations.append(ReplaceDataNumericalValues())
        self.transformations = transformations

    def generate(self, input: object, data_subset: str, dataset_size=None):
        generations = {}
        for transformation in self.transformations:
            output = "Transforming input with: {}".format(transformation.name())
            generations[transformation.name()] = transformation.generate(input, data_subset, dataset_size)

            if generations[transformation.name()]:
                output = output + " -- SUCCEEDED"
            else:
                output = output + " -- FAILED"
            print(output)
        return generations
