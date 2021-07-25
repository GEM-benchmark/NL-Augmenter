from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformers import pipeline, set_seed

"""
Adds generated sentence into provided sentences or paragraph to create adversarial examples.
"""


class SentenceAdditions(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    heavy = True

    def __init__(self, seed=42, max_outputs=1, max_length=30, model='gpt2-xl'):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.model = model
        self.max_outputs = max_outputs
        self.max_length = max_length

    def generate(self, sentence: str):
        perturbed = self.sentence_additions(text=sentence)
        return perturbed

    def sentence_additions(self, text):
        set_seed(self.seed)
        generator = pipeline('text-generation', model=self.model)
        outputs = generator(text, max_length = self.max_length, num_return_sequences = self.max_outputs)
        perturbed = []
        for sents_with_additions in outputs:
            for key, value in sents_with_additions.items():
                perturbed.append(value)

        return perturbed
