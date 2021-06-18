from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import numpy as np

class SwapCharactersPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str, prob = .05):
        pertubed = self.swap_characters(text=sentence, prob=prob, seed=self.seed)
        return pertubed

    def swap_characters(self, text, prob=0.05, seed=0):
        max_seed = 2**32
        # seed with hash so each text of same length gets different treatment
        np.random.seed((seed + sum([ord(c) for c in text])) % max_seed)
        # np.random.seed((seed) % max_seed)
        # number of possible characters to swap.
        num_pairs = len(text) - 1
        # if no pairs, do nothing
        if num_pairs < 1:
            return text
        # get indices to swap
        indices_to_swap = np.argwhere(np.random.rand(num_pairs) < prob).reshape(-1)
        # shuffle swapping order, may matter if there are adjacent swaps
        np.random.shuffle(indices_to_swap)
        # convert to list
        text = list(text)
        # swap
        for index in indices_to_swap:
            text[index], text[index+1] = text[index+1], text[index]
        # convert to string
        text = ''.join(text)
        return text
