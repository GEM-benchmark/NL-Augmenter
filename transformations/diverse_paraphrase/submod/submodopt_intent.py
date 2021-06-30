import numpy as np
import scipy.linalg as la
import pdb
from collections import Counter
import string

from transformations.diverse_paraphrase.submod.submodular_funcs import distinct_ngrams


class SubmodularOpt:
    def __init__(self, V=None, A=None, A_=None, **kwargs):
        self.A = A
        self.A_ = A_
        self.V = V

    def initialize_function(self, lam=0.5, a1=1.0, a2=1.0, b1=1.0, b2=1.0):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2

        self.ndistinct_norm = distinct_ngrams(self.V)
        self.lam = lam

    def final_func(self, pos_sets, rem_list, selec_set):
        distinct_score = (
            np.array(list(map(distinct_ngrams, pos_sets))) / self.ndistinct_norm
        )
        diversity_score = self.b1 * distinct_score
        final_score = diversity_score

        return final_score

    def maximize_func(self, k=5):
        selec_sents = set()
        ground_set = set(self.V)
        selec_set = set(selec_sents)
        rem_set = ground_set.difference(selec_set)
        while len(selec_sents) < k:

            rem_list = list(rem_set)
            pos_sets = [list(selec_set.union({x})) for x in rem_list]

            score_map = self.final_func(pos_sets, rem_list, selec_set)
            max_idx = np.argmax(score_map)

            selec_sents = pos_sets[max_idx]
            selec_set = set(selec_sents)
            rem_set = ground_set.difference(selec_set)

        return selec_sents
