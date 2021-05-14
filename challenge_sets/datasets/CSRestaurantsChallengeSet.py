from challenge_sets.ChallengeSetTransformation import ChallengeSetTransformation
from common.cs_restaurants.CSEntry import CSEntry
from collections import defaultdict


class CSRestaurantsChallengeSet(ChallengeSetTransformation):

    def generate(self, dataset: object):
        if isinstance(dataset, dict):
            return {"challenge_acts": self.challenge_acts(dataset),
                    "challenge_input_size": self.challenge_input_size(dataset)}

    def challenge_acts(self, restaurants):
        "Compare different acts."
        challenge_set = defaultdict(list)
        for entry in restaurants['test']:
            info = CSEntry(entry)
            challenge_set[info.dialog_act].append(entry['gem_id'])
        return challenge_set

    def challenge_input_size(self, restaurants):
        "Compare items with different input sizes."
        challenge_set = defaultdict(list)
        for entry in restaurants['test']:
            info = CSEntry(entry)
            preds = tuple(sorted(info.lexicalised.keys()))
            challenge_set[f"input_length_{len(preds)}"].append(entry['gem_id'])
        return challenge_set