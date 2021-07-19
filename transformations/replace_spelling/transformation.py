import itertools
import random
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def generate_sentence(sentence, spell_errors, prob_of_typo, seed):
    output = []
    for word in sentence.split():
        random.seed(seed)
        if word.lower() in list(spell_errors.keys()) and random.choice(range(0, 100)) <= prob_of_typo:
            output.append(random.choice(spell_errors[word.lower()]))
        else:
            output.append(word)
    output = " ".join(output)
    return output


def generate_sentences(text, prob=0.1, seed=0, max_outputs=1):
    spell_errors = os.path.join('transformations', 'replace_spelling', 'spell_errors.json')
    with open(spell_errors, 'r') as fp:
        spell_errors = json.load(fp)

    prob_of_typo = int(prob * 100)

    perturbed_texts = []
    for idx in range (max_outputs):
        new_text = generate_sentence(text, spell_errors, prob_of_typo, seed+idx)
        perturbed_texts.append(new_text)
    return perturbed_texts


class SpellingTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        perturbed_texts = generate_sentences(text=sentence,
                                            prob=0.20,
                                            seed=self.seed,
                                            max_outputs=self.max_outputs,
                                            )
        return perturbed_texts

if __name__ == '__main__':
    from TestRunner import convert_to_snake_case

    sentences =  [
    "Andrew finally returned the French book to Chris that I bought last week",
    "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
    "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
    "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
    "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization." ]


    tf = SpellingTransformation(max_outputs=3)

    def generate_json(sentences):
        test_cases = []
        for sentence in sentences:
            outputs = [{"sentence": o} for o in tf.generate(sentence)]
            test_cases.append(
            {
            "class": tf.name(),
            "inputs": {"sentence": sentence},
                "outputs": outputs}
            )
        json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
        return json_file

    json_file = generate_json(sentences)

    f = os.path.join('transformations', 'replace_spelling', 'test.json')
    with open(f, 'w') as fp:
        json.dump(json_file, fp, indent=2)
