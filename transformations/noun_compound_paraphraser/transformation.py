import random

import os
import json

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def noun_compound_paraphraser(text, compounds):

    L = [[text]]
    for k in compounds.keys():
        if k in L[0][0]:
            new = []
            for l in L:
                for text in l:
                    n = [text.replace(k,paraphrase[0]) for paraphrase in compounds[k]]
                    new.extend(n)
            L.append(new)
    # Flatten the list and ignore the first (the original text)
    paraphrases = [x for u in L[1:] for x in u]

    return paraphrases


class NounCompoundParaphraser(SentenceOperation):
    """Replaces two-word noun compounds with a paraphrase.

    Args:
        max_paraphrases: Maximimum number of paraphrases per noun compound.
            All combinations of paraphrases will be returned whenever more
            than one noun compound from the dictionary is found in the sentence.
            Default: 1.
        seed: initial seed. Defaults: 0.
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_paraphrases=1):
        super().__init__(seed)

        data_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data"
        )

        with open(os.path.join(data_dir, 'compound_paraphrases_semeval2013_task4.json'),'r') as fd:
            compound_paraphrases = json.load(fd)

        # Trim to only use up to `max_paraphrases` per compound. When sorting,
        # by paraphrase score (frequency), randomly break ties.
        random.seed(seed)
        for k in compound_paraphrases.keys():
            randomized_ties = sorted(compound_paraphrases[k],  key=lambda i: (int(i[1]), random.random()  ) , reverse=True)
            compound_paraphrases[k] = randomized_ties[:max_paraphrases]

        self.compound_paraphrases = compound_paraphrases

    def generate(self, sentence):
        perturbed_texts = noun_compound_paraphraser(
            text=sentence,
            compounds=self.compound_paraphrases,
        )
        return perturbed_texts
