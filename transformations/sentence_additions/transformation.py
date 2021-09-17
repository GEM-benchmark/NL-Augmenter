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

    keywords = ["discourse", "model-based", "transformer-based", "visual", "possible-meaning-alteration", "high-generations"]
    heavy = True

    def __init__(self, seed=0, max_outputs=1, max_length=75, model='gpt2-xl'):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.model = model
        self.max_outputs = max_outputs
        self.max_length = max_length

    def generate(self, sentence: str, prompt_text=" PARAPHRASE: ", prompt=False):
        perturbed = self.sentence_additions(text=sentence, prompt_text=prompt_text, prompt=prompt)
        return perturbed

    def sentence_additions(self, text, prompt_text, prompt):
        set_seed(self.seed)
        generator = pipeline('text-generation', model=self.model)
        if(prompt):
            text = text + prompt_text
        outputs = generator(text, max_length = self.max_length, num_return_sequences = self.max_outputs)
        perturbed = []
        for sents_with_additions in outputs:
            for key, value in sents_with_additions.items():
                perturbed.append(value)

        return perturbed

# For testing outputs
if __name__ == "__main__":
    sentence_addition = SentenceAdditions()
    text = "Trinity Medical Imaging is one of the foremost providers of private nuclear medicine imaging in London and Surrey. We work with the finest nuclear medicine consultants from a wide variety of specialist fields."
    new_text = sentence_addition.generate(text, prompt=True)
    print(new_text)
