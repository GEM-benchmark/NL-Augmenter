from typing import List, Tuple

import spacy

from nlaugmenter.common.initialize import spacy_nlp
from nlaugmenter.interfaces.SentencePairOperation import SentencePairOperation
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.transformations.back_translation import BackTranslation

"""
This generates counterfactuals using a simple rule based approach which would be
beneficial for paraphrase generation tasks.
Assumes text pairs are labelled "1" for semantically similar and "0" for dissimilar.
This is an example generator.
"""


def get_tokens_of_pos_type(sentence, types: list):
    tokens = []
    for token in sentence:
        if token.pos_ in types:
            tokens.append(token)
    return tokens


class LexicalCounterfactualGenerator(SentencePairOperation):
    tasks = [TaskType.PARAPHRASE_DETECTION]
    languages = ["en"]
    to_avoid = [
        "no",
        "not",
        "nowhere",
        "hardly",
        "barely",
        "nobody",
        "none",
        "nothing",
        "neither",
        "nowhere",
        "never",
        "scarcely",
        "n't",
        "nt",
    ]

    def __init__(self, seed=0, max_outputs=2, pos_label="1", neg_label="0"):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.pos_label = pos_label
        self.neg_label = neg_label
        self.bt = BackTranslation()

    def negate_if_single_verb(self, sentence):
        """
        This only negates single verb sentences to be precise. This should be later extended to multiple verbs.
        Eventually backtranslates the sentence to repair grammatical errors.
        """
        if "not " in sentence.split(" "):
            return [sentence]
        doc = self.nlp(sentence)
        verbs = get_tokens_of_pos_type(doc, ["VERB"])
        if len(verbs) == 1:
            tokens = []
            for token in doc:
                if token.text in self.to_avoid:
                    # do not generate if a negated word is present
                    return [sentence]
                if token.pos_ in ["VERB"]:
                    tokens.append("not")
                tokens.append(token.text)
            basic_negated_sentence = " ".join(tokens)
            return self.bt.generate(basic_negated_sentence)
        return [sentence]

    def generate(
        self, sentence1: str, sentence2: str, target: str
    ) -> List[Tuple[str, str, str]]:
        """
        This implementation augments data for semantic similarity tasks.
        This converts pairs which are positive (i.e. paraphrases-> label:1) to non-paraphrases (label:0).
        """
        examples = []
        if target == self.pos_label:
            for sentence1_n in self.negate_if_single_verb(sentence1):
                if sentence1_n != sentence1:
                    examples.append((sentence1_n, sentence2, self.neg_label))
            for sentence2_n in self.negate_if_single_verb(sentence2):
                if sentence2_n != sentence2:
                    examples.append((sentence1, sentence2_n, self.neg_label))
            if len(examples) > 0:
                return examples
        return [(sentence1, sentence2, target)]


# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = LexicalCounterfactualGenerator(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence1, sentence2 in zip(
        [
            "Andrew finally returned the French book to Chris",
            "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate.",
            "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
            "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
            "The fighters would never give up.",
            "Neuroplasticity allows short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
        ],
        [
            "In the end returned the French book to Chris",
            "Gapping sentences, such as Paul likes coffee and Mary tea, do not have an overt predicate.",
            "Alice in Wonderland is an American animated, dark fantasy adventure film from 2010",
            "U.D. Dosanjh was the 33rd Premier of British Columbia for a year from 2000",
            "The warriors wouldn't leave the battlefield.",
            "Neuroplasticity permits short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
        ],
    ):
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {
                    "sentence1": sentence1,
                    "sentence2": sentence2,
                    "target": "1",
                },
                "outputs": [
                    {"sentence1": o[0], "sentence2": o[1], "target": o[2]}
                    for o in tf.generate(sentence1, sentence2, "1")
                ],
            }
        )
    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    with open("test.json", "w") as f:
        json.dump(json_file, f, indent=2)
