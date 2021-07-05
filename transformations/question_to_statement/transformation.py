from typing import Tuple, List
import nltk
from pyinflect import getInflection
import spacy
import numpy as np


from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class QuestionToStatement(SentenceOperation):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TAGGING,
    ]

    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        np.random.seed(seed)
        nltk.download("punkt")

        self.seed = seed
        self.max_output = max_output

        self.nlp = spacy.load("en_core_web_sm")

    def _transform(self, question):
        text = nltk.word_tokenize(question)
        doc = self.nlp(question)
        modal = str(doc[0]).lower()
        token = doc[0]

        modal_position = token.head.i
        for tok in token.head.lefts:
            if tok.dep_ == "advmod":
                modal_position = tok.i
                break

        rest_of_sentence = text[modal_position:]

        if text[1].lower() == "n't":
            text = text[1:]
            doc = doc[1:]
            modal_position = modal_position - 1

        beginning = [text[1].capitalize()]
        beginning.extend(text[2:modal_position])
        sentence = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(
            beginning + rest_of_sentence
        )

        first_verb = token.head
        if modal == "did":
            demodded = first_verb._.inflect("VBD")
        else:
            first_verb = doc[modal_position]
            demodded = modal + " " + str(first_verb)
        sentence = sentence.replace(str(first_verb), str(demodded)).replace("?", "")

        return sentence

    def _filter_phrase(self, question):
        try:
            if question.strip()[-1] != "?":
                return False
        except IndexError:
            return False

        if " or " in question:
            return False

        doc = self.nlp(question)
        token = doc[0]
        if token.pos_ != "AUX":
            return False

        return True

    def generate(self, sentence: str):
        if not self._filter_phrase(sentence):
            return [sentence]

        paraphrased = self._transform(sentence)
        return [sentence, paraphrased]


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = QuestionToStatement()

    test_cases = []
    for i, sentence in enumerate(
        [
            "Did Sally finally return the french book to Chris?",
            "Did the American National Shipment company really break its own fleet?",
            "Couldn't she just quickly leave?",
            "Shall you begone, lad?",
            "Has Buzz Aldrin, the first person who walked on the moon, brought back some aliens?",
        ]
    ):
        res = tf.generate(sentence)
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": i} for i in res],
            }
        )

    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
