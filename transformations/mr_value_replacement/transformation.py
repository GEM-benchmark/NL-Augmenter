import random
from itertools import product
from random import sample

import spacy
import torch
import torchtext.vocab

from common.initialize import glove, spacy_nlp
from interfaces.KeyValuePairsOperation import KeyValuePairsOperation
from tasks.TaskTypes import TaskType


class MRValueReplacement(KeyValuePairsOperation):
    tasks = [TaskType.E2E_TASK]
    languages = ["en"]
    heavy = True

    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "highly-meaning-preserving",
        "high-precision",
    ]

    def __init__(self, seed=0, n_similar=10, max_outputs=1):
        """Method for initializing tools and setting variables."""

        super().__init__(seed, max_outputs=max_outputs)

        self.glove = (
            glove if glove else torchtext.vocab.GloVe(name="6B", dim="100")
        )
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

        self.max_outputs = max_outputs
        self.n_similar = n_similar

    def generate(self, meaning_representation: dict, reference: str):
        """Method for generating variatios of the MR/utterances."""

        outputs = []
        candidate_alignments = self.get_alignments(
            meaning_representation, reference
        )

        if len(candidate_alignments) == 0:
            return outputs

        closest_set = []
        for candidate in candidate_alignments:
            closest = self.closest_words(
                candidate[1].lemma_.lower(), self.n_similar
            )

            if closest is not None:
                closest_set.append(closest)
            else:
                closest_set.append([meaning_representation[candidate[0]]])

        if len(closest_set) == 0:
            return outputs

        products = list(product(*closest_set))

        random.seed(self.seed)
        sample_output = sample(products, self.max_outputs)

        for output_instance in sample_output:
            mr = meaning_representation.copy()
            ref = reference
            for candidate, replacement in zip(
                candidate_alignments, output_instance
            ):
                mr[candidate[0]] = replacement
                ref = ref.replace(candidate[1].text, replacement)
            outputs.append((mr, ref))

        return outputs

    def get_alignments(self, meaning_representation, reference):
        """Method for extracting the alignments between MR values and the tokens in reference."""

        tokens = self.nlp(reference)
        candidate_alignments = []
        for key, value in meaning_representation.items():
            for token in tokens:
                if (
                    len(value.split()) == 1
                    and value.lower() == token.lemma_.lower()
                ):
                    candidate_alignments.append((key, token))

        return candidate_alignments

    def get_vector(self, word):
        """Method for extracting a word vector"""

        if word in self.glove.stoi:
            return self.glove.vectors[self.glove.stoi[word]]
        else:
            return None

    def closest_words(self, word, n):
        """Method for recovering a specific number of similar words according to a word."""

        vector = self.get_vector(word)

        if vector is None:
            return None

        distances = [
            (w, torch.dist(vector, self.get_vector(w)).item())
            for w in self.glove.itos
        ]

        return [w for w, v in sorted(distances, key=lambda w: w[1])[:n]]
