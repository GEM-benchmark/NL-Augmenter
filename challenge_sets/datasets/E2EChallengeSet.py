from challenge_sets.ChallengeSetTransformation import ChallengeSetTransformation
from collections import defaultdict


class E2EChallengeSet(ChallengeSetTransformation):

    def generate(self, dataset: object):
        if isinstance(dataset, dict):
            return {"challenge_input_size": self.challenge_input_size(dataset),
                    "challenge_reference_size": self.challenge_reference_size(dataset)}

    def challenge_input_size(self, dataset):
        "Compare items with different input sizes."
        challenge_set = defaultdict(list)
        for entry in dataset['test']:
            challenge_set[f"input_length_{len(entry['meaning_representation'].split(', '))}"].append(entry['gem_id'])
        return challenge_set

    def challenge_reference_size(self, dataset):
        "Compare items with different reference text length"
        challenge_set = defaultdict(list)
        for entry in dataset['test']:
            challenge_set[f"ref_length_{len(entry['references'][0])}"].append(entry['gem_id'])
        return challenge_set

