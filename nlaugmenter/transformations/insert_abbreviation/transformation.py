import os

import nlaugmenter.transformations.insert_abbreviation.grammaire as grammaire
from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

# sys.path.append("./transformations/insert_abbreviation")


def readfile(file):
    with open(file, encoding="utf8") as input:
        lines = input.readlines()
    return lines


def load_rules(file):
    with open(file, encoding="utf8") as input:
        str_rules = input.read()
    return str_rules


"""
Abbreviations
"""


class AbbreviationInsertionEN(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        current_path = os.path.realpath(__file__).replace(
            os.path.basename(__file__), ""
        )
        rulefile_en = f"{current_path}replacement_rules_en.txt"
        super().__init__(seed, max_outputs=max_outputs)
        rules_en = load_rules(rulefile_en)
        # First we compile our rules...
        self.grammar_en = grammaire.compile(rules_en)

    def generate(self, sentence: str):
        results = grammaire.parse(sentence, self.grammar_en)
        # We now replace the strings with their label
        perturbed_texts = sentence
        # Each list in results is an element such as: [label, [left,right]]
        # label pertains from rules
        # left is the left offset of the isolated sequence of words
        # right is the right offset of the isolated sequence of words
        # elements are stored from last to first in the text along the offsets
        for v in results:
            from_token = v[1][0]
            to_token = v[1][1]
            perturbed_texts = (
                perturbed_texts[:from_token]
                + v[0]
                + perturbed_texts[to_token:]
            )
        return [perturbed_texts]


class AbbreviationInsertionFR(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["fr"]

    def __init__(self, seed=0, max_outputs=1):
        current_path = os.path.realpath(__file__).replace(
            os.path.basename(__file__), ""
        )
        rulefile_fr = f"{current_path}replacement_rules_fr.txt"
        super().__init__(seed, max_outputs=max_outputs)
        rules_fr = load_rules(rulefile_fr)
        # First we compile our rules...
        self.grammar_fr = grammaire.compile(rules_fr)

    def generate(self, sentence: str):
        results = grammaire.parse(sentence, self.grammar_fr)
        # We now replace the strings with their label
        perturbed_texts = sentence
        # Each list in results is an element such as: [label, [left,right]]
        # label pertains from rules
        # left is the left offset of the isolated sequence of words
        # right is the right offset of the isolated sequence of words
        # elements are stored from last to first in the text along the offsets
        for v in results:
            from_token = v[1][0]
            to_token = v[1][1]
            perturbed_texts = (
                perturbed_texts[:from_token]
                + v[0]
                + perturbed_texts[to_token:]
            )
        return [perturbed_texts]


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = AbbreviationInsertion()
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
"""
