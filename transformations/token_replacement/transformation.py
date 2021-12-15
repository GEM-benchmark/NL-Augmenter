import random
from typing import List

from spacy import load as spacy_load

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.token_replacement.lookup_table_utils import (
    get_token_replacement,
    load_lookup,
)

"""
Implementation of the token replacement perturbation using lookup tables
with valid replacement candidates
"""


class TokenReplacement(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        replacement_prob=0.2,
        min_length=3,
        max_dist=1,
        lookup=["typos.xz", "ocr.xz"],
    ):
        """
        :param seed: random seed
        :param max_outputs: max. number of outputs to generate
        :param replacement_prob: replacement probability [0.0, 1.0]
        :param min_length: min. length of token that can be perturbed
        :param max_dist: max. Levenshtein distance between the original and the
                         perturbed token
        :param lookup: dictionary or a list of files with lookup tables
        """
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy_load("en_core_web_sm")
        self.replacement_prob = replacement_prob
        self.max_dist = max_dist
        self.min_length = min_length

        if isinstance(lookup, dict):
            self.lookup = lookup
        else:
            self.lookup = load_lookup(lookup)

    def generate(self, sentence: str) -> List[str]:

        random.seed(self.seed)

        perturbed_sentences = []

        for _ in range(self.max_outputs):

            perturbed_tokens = []
            doc = self.nlp(sentence)

            tok_status = [
                tok.text in self.lookup and len(tok.text) >= self.min_length
                for tok in doc
            ]
            cnt_with_repl = sum(tok_status)

            # replacement probability weighted by the ratio of tokens that have
            # at least one replacement candidate and min. required length
            prob_weighted = (
                min(1.0, self.replacement_prob * len(doc) / cnt_with_repl)
                if cnt_with_repl > 0
                else 0.0
            )

            # print(f"prob_weighted = {prob_weighted:.2f} (all={len(doc)} cnt_with_repl={cnt_with_repl})")

            for tok_idx, tok in enumerate(doc):

                text = tok.text

                p = random.random()
                if tok_status[tok_idx] and p <= prob_weighted:
                    text = get_token_replacement(
                        text, self.lookup, self.max_dist
                    )

                # print(f"'{tok.text}' -> '{text}' diff={tok.text != text} [status={tok_status[tok_idx]}] (p={p:.2f})")

                if tok.whitespace_:
                    text += " "

                perturbed_tokens.append(text)

            perturbed_sentences.append(
                "".join(token for token in perturbed_tokens)
            )

        return perturbed_sentences


# Sample code to demonstrate usage. Can also assist in adding test cases.

if __name__ == "__main__":

    import json
    import os

    from TestRunner import convert_to_snake_case

    tf = TokenReplacement(max_outputs=1)
    test_cases = []
    src = [
        "Manmohan Singh served as the PM of India.",
        "Neil Alden Armstrong was an American astronaut.",
        "Katheryn Elizabeth Hudson is an American singer.",
        "The owner of the mall is Anthony Gonsalves.",
        "Roger Michael Humphrey Binny (born 19 July 1955) is an Indian "
        + "former cricketer.",
    ]

    for idx, sent in enumerate(src):
        outputs = tf.generate(sent)
        test_cases.append(
            {"class": tf.name(), "inputs": {"sentence": sent}, "outputs": []}
        )
        for out in outputs:
            test_cases[idx]["outputs"].append({"sentence": out})

    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    # print(json.dumps(json_file))

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, "test.json"), "w") as f:
        json.dump(json_file, f, indent=2, ensure_ascii=False)
