from challenge_sets.ChallengeSetTransformation import ChallengeSetTransformation
from challenge_sets.datasets.WebNLGChallengeSet import WebNLGChallengeSet
from challenge_sets.datasets.CSRestaurantsChallengeSet import CSRestaurantsChallengeSet
from challenge_sets.datasets.E2EChallengeSet import E2EChallengeSet


class ChallengeSetList(ChallengeSetTransformation):

    def __init__(self):
        transformations = []
        transformations.append(WebNLGChallengeSet())
        transformations.append(CSRestaurantsChallengeSet())
        transformations.append(E2EChallengeSet())
        self.transformations = transformations

    def generate(self, input: dict):
        generations = {}
        for transformation in self.transformations:
            if transformation.name() in input.keys():
                output = "Transforming input with: {}".format(transformation.name())
                generations[transformation.name()] = transformation.generate(input[transformation.name()])

                print(generations)

                if generations[transformation.name()]:
                    output = output + " -- SUCCEEDED"
                else:
                    output = output + " -- FAILED"
                print(output)
        return generations

