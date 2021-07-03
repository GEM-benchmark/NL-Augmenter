import random

import sys
sys.path.append('../..')
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def whitespace(text, remove_prob=0.1, add_prob=0.05, seed=0):
    random.seed(seed)
    newtext = []
    for char in text:
        random_num = random.random()
        if char.isspace() and random_num < remove_prob:
            continue
        newtext.append(char)
        if (not char.isspace()) and random_num < add_prob:
            newtext.append(' ')

    return ''.join(newtext)


class WhitespacePerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en", "es", "de", "fr", "it"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = whitespace(text=sentence, remove_prob=0.1, add_prob=0.05, seed=self.seed)
        return pertubed

# """
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json

    tf = WhitespacePerturbation()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": {"sentence": tf.generate(sentence)}}
        )

    # json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(test_cases, indent=2))
# """