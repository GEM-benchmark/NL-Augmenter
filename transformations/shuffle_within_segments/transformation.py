import itertools
import random
from typing import List, Tuple

import numpy as np

from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType


class ShuffleWithinSegments(TaggingOperation):
    """
    Shuffling tokens within segments.

    The token sequence is split into segments of the same label;
    for each segment, a decision is made randomly: to shuffle it or not.
    In case of a positive decision, the tokens within each segment are shuffled.

    """
    tasks = [TaskType.TEXT_TAGGING]
    languages = "All"
    keywords = ["lexical",
                "word-order",
                "rule-based",
                "unnaturally-written",
                "unnatural-sounding",
                "possible-meaning-alteration",
                "high-precision",
                "low-coverage",
                "low-generations"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(
            self, token_sequence: List[str], tag_sequence: List[str]
    ) -> List[Tuple[List[str], List[str]]]:

        # it is necessary to set up numpy random seed due to np.random.binomial
        np.random.seed(self.seed)
        token_seq = token_sequence.copy()
        tag_seq = tag_sequence.copy()
        perturbed_sentences = []

        assert len(token_seq) == len(
            tag_seq
        ), "Lengths of `token_seq` and `tag_seq` should be the same"

        # we need the original indices of each tag
        tags = [(i, t) for i, t in enumerate(tag_seq)]

        # split the tags into the segments with the same label
        groups = [list(g) for k, g in itertools.groupby(tags, lambda s: s[1].split('-')[-1])]

        for _ in itertools.repeat(None, self.max_outputs):
            new_tokens = []

            for group in groups:
                # now we need only indices of each group
                indices = [i[0] for i in group]

                if np.random.binomial(1, 0.5):
                    np.random.shuffle(indices)

                new_tokens.extend([token_seq[idx] for idx in indices])

            perturbed_sentences.append((new_tokens, tag_seq))

        return perturbed_sentences
