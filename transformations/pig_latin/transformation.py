import piglatin
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

class PigLatin(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1, replace_prob=1.0):
        super().__init__(seed, max_outputs=max_outputs)
        self.replace_prob = replace_prob

    def generate(self, sentence: str):
        piglatin_sentences = []
        for _ in range(self.max_outputs):
            piglatin_sentence = []
            for word in sentence.lower().split():
                if random.random() < self.replace_prob:
                    new_word = piglatin.translate(word)
                else:
                    new_word = word
                piglatin_sentence.append(new_word.replace('-', ''))
            piglatin_sentence = ' '.join(piglatin_sentence)
            piglatin_sentences.append(piglatin_sentence)
        return piglatin_sentences
