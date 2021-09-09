import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def add_spaces(text, prob_token=0.1, prob_char=1.0, seed=0, max_outputs=1):
    random.seed(seed)

    words = text.split(" ")
    perturbed_texts = []
    for _ in range(max_outputs):
        perturbed_text = []
        for word in words:
            if random.random() <= prob_token:
                if prob_char == 1:
                    new_word = " ".join(word)
                else:
                    new_word = [word[0]]
                    for letter in word[1:]:
                        if random.random() <= prob_char:
                            new_word.append(" ")
                        new_word.append(letter)
                new_word = "".join(new_word)
            else:
                new_word = word
            perturbed_text.append(new_word)
        perturbed_texts.append(" ".join(perturbed_text))
    return perturbed_texts


class SpaceBetweenCharacters(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["all"]

    def __init__(self, seed=42, max_outputs=1, prob_token=0.1, prob_char=1.0):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob_token = prob_token
        self.prob_char = prob_char

    def generate(self, sentence: str) -> List[str]:
        perturbed_texts = add_spaces(
            text=sentence,
            prob_token=self.prob_token,
            prob_char=self.prob_char,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
