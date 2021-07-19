import itertools
import random
import json
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from TestRunner import convert_to_snake_case
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

def get_syn(word, seed):
    random.seed(seed)
    dot = False
    if word.endswith('.'): # to check last word of the sentence
        dot = True
        word = word[:-1]
    syns = wordnet.synsets(word.lower())

    if len(syns) > 0:
        form = syns[0].pos()
        syns = [syn.lemmas()[0].name() for syn in syns if syn.pos()==form]
        syn = random.choice(syns)
        if dot:
            syn = syn + '.'
        return syn
    else:
        if dot:
            return word + '.'
        else:
            return word

    return syn


def generate_sentence(sentence, prob, seed):
    random.seed(seed)
    output = []
    for word in sentence.split():

        if random.choice(range(0, 100)) <= prob and len(word) > 4:
            syn = get_syn(word, seed)
            output.append(syn)
        else:
            output.append(word)
    output = " ".join(output)
    return output


def generate_sentences(text, prob=0.1, seed=0, max_outputs=1):

    prob = int(prob * 100)

    perturbed_texts = []
    for idx in range (max_outputs):
        new_text = generate_sentence(text, prob, seed+idx)
        perturbed_texts.append(new_text)
    return perturbed_texts


class SynonymTransformation(SentenceOperation):
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
                                            prob=0.80,
                                            seed=self.seed,
                                            max_outputs=self.max_outputs,
                                            )
        return perturbed_texts

if __name__ == '__main__':

    sentences =  [
    "All the persons we work with are incredibly awesome.",
    "Thailand has imposed a nationwide ban on public gatherings.",
    "The chances of reversing this situation are becoming more distant by the day.",
    "Your speech was awesome today.",
    "Banks report bumper second-quarter profits." ]
    print(sentences)

    tf = SynonymTransformation(max_outputs=3)

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

    f = os.path.join('transformations', 'replace_synonym', 'test.json')
    with open(f, 'w') as fp:
        json.dump(json_file, fp, indent=2)
