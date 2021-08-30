import piglatin

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

class PigLatin(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        output_sentence = piglatin.translate(sentence.lower())
        piglatin_sentence = []
        for word in output_sentence.split():
            piglatin_sentence.append(word.replace('-', ''))
        piglatin_sentence = ' '.join(piglatin_sentence)
        return [piglatin_sentence]
