import itertools
import random
import spacy
import numpy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from SoundsLike.SoundsLike import Search
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def close_homophones_swap(text, corrupt_prob, seed=0, max_output=1):
    random.seed(seed)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    perturbed_texts = []
    spaces = [True if tok.whitespace_ else False for tok in doc]
    for _ in range(max_output):
        perturbed_text = []
        for index, token in enumerate(doc):
            if random.uniform(0, 1) < corrupt_prob:
                try:
                    replacement = random.choice(Search.closeHomophones(token.text))
                    perturbed_text.append(replacement)
                except:
                    perturbed_text.append(token.text)
            else:
                perturbed_text.append(token.text)
        
        textbf = []             
        for index, token in enumerate(perturbed_text):
            textbf.append(token)
            if spaces[index]:
                textbf.append(' ')
        perturbed_texts.append(''.join(textbf))
    return perturbed_texts
       
class CloseHomophonesSwap(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        self.max_output = max_output

    def generate(self, sentence: str):
        perturbed_texts = close_homophones_swap(
            text=sentence, corrupt_prob=0.5, seed=self.seed, max_output=self.max_output
        )
        return perturbed_texts



# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = CloseHomophonesSwap(max_output=1)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
