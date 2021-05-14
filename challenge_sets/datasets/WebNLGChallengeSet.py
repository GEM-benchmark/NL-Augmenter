from challenge_sets.ChallengeSetTransformation import ChallengeSetTransformation
from collections import defaultdict
from common.webnlg.Triple import Triple


class WebNLGChallengeSet(ChallengeSetTransformation):

    def generate(self, dataset: object):
        if isinstance(dataset, dict):
            return {"challenge_input_size": self.challenge_input_size(dataset),
                    "challenge_single_predicates": self.challenge_single_predicates(dataset),
                    "challenge_combinations": self.challenge_combinations(dataset),
                    "challenge_args": self.challenge_args(dataset)}

    def get_triples(self, entry):
        return [Triple(triple_text) for triple_text in entry['input']]

    def challenge_input_size(self, dataset):
        "Compare items with different input sizes."
        challenge_set = defaultdict(list)
        for entry in dataset['test']:
            challenge_set[f"input_length_{len(entry['input'])}"].append(entry['gem_id'])
        return challenge_set

    def challenge_single_predicates(self, dataset):
        "Compare seen and unseen single predicates."
        challenge_set = defaultdict(list)
        train_preds = set()
        for entry in dataset['train']:
            triples = self.get_triples(entry)
            train_preds.update([triple.prop for triple in triples])

        for entry in dataset['test']:
            triples = self.get_triples(entry)
            if len(triples) == 1:
                if triples[0].prop in train_preds:
                    challenge_set['seen'].append(entry['gem_id'])
                else:
                    challenge_set['unseen'].append(entry['gem_id'])
        return challenge_set

    def challenge_combinations(self, dataset):
        "Compare seen and unseen combinations of predicates."
        challenge_set = defaultdict(list)
        train_combos = set()
        for entry in dataset['train']:
            triples = self.get_triples(entry)
            if len(triples) > 1:
                current_tuple = tuple([triple.prop for triple in triples])
                train_combos.add(current_tuple)
        for entry in dataset['test']:
            triples = self.get_triples(entry)
            if len(triples) > 1:
                current_tuple = tuple([triple.prop for triple in triples])
                if current_tuple in train_combos:
                    challenge_set['seen'].append(entry['gem_id'])
                else:
                    challenge_set['unseen'].append(entry['gem_id'])
        return challenge_set

    def challenge_args(self, dataset):
        "Compare inputs based on whether all arg1s and arg2s were seen or not."
        challenge_set = defaultdict(list)
        train_arg1s = {triple.subj for entry in dataset['train']
                       for triple in self.get_triples(entry)}
        train_arg2s = {triple.obj for entry in dataset['train']
                       for triple in self.get_triples(entry)}
        for entry in dataset['test']:
            triples = self.get_triples(entry)
            arg1s = {triple.subj for triple in triples}
            arg2s = {triple.obj for triple in triples}
            unseen_arg1 = arg1s - train_arg1s
            unseen_arg2 = arg2s - train_arg2s
            if unseen_arg1 and unseen_arg2:
                challenge_set['both_unseen'].append(entry['gem_id'])
            elif unseen_arg1:
                challenge_set['arg1_unseen'].append(entry['gem_id'])
            elif unseen_arg2:
                challenge_set['arg2_unseen'].append(entry['gem_id'])
            else:
                challenge_set['both_seen'].append(entry['gem_id'])
        return challenge_set