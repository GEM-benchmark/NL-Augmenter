import itertools

import spacy

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""
"""
Yoda Speak implementation borrowed from here: https://github.com/yevbar/Yoda-Script, with minor mofifications to fix
deprecation and to change some stylistic features
"""


class YodaPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "word-order",
        "model-based",
        "unnatural-sounding",
        "highly-meaning-preserving",
        "high-coverage",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.comma = self.nlp(" , ")[1]
        self.punctuation = [",", ".", ";", "?", "!"]

    def generate(self, sentence: str):
        perturbed_texts = list(
            itertools.repeat(self.yoda(sentence), self.max_outputs)
        )
        return perturbed_texts

    def sentify(self, text):
        """
        Takes an input text, splits it into sentences, and applies a yoda transformation to individual clauses in the sentence
        """
        output = []
        doc = self.nlp(text)
        for sent in doc.sents:
            sentence = []
            for clause in self.clausify(sent):
                sentence.append(self.yodafy(clause))
            output.append(sentence)
        return output

    def clausify(self, sent):
        """
        Turns sentences into clauses
        """
        output = []
        cur = []
        for token in sent:
            if token.dep_ == "cc" or (
                token.dep_ == "punct" and token.text in self.punctuation
            ):
                output.append(cur)
                output.append([token])
                cur = []
            else:
                cur.append(token)
        if cur != []:
            output.append(cur)
        return output

    def yodafy(self, clause):
        """
        Takes each clause and puts it into yoda format
        """
        new_array = []
        state = False
        for token in clause:
            if state:
                new_array.append(token)
            if not state and (token.dep_ == "ROOT" or token.dep_ == "aux"):
                state = True
        if (
            len(new_array) > 0
            and new_array[len(new_array) - 1].dep_ != "punct"
        ):
            new_array.append(self.comma)
        for token in clause:
            new_array.append(token)
            if token.dep_ == "ROOT" or token.dep_ == "aux":
                break
        return new_array

    def yoda(self, s):
        """
        Takes an input sentence and rearranges it in "Yoda-speak"

        inputs:
        s: string

        returns: string
        """
        string = []
        yodafied = self.sentify(s)
        for sentence in yodafied:
            sent = ""
            for clause in sentence:
                for token in clause:
                    if token.dep_ in ["NNP", "NNPS"] or token.text == "I":
                        sent += token.text + " "
                    elif sent == "":
                        if token.dep_ == "neg":
                            sent += "Not" + " "
                        else:
                            sent += (
                                token.text[0].upper() + token.text[1:] + " "
                            )
                    elif token.dep_ == "punct":
                        sent = sent[: len(sent) - 1] + token.text + " "
                    else:
                        if token.pos_ == "PROPN":
                            sent += token.text + " "
                        else:
                            sent += token.text.lower() + " "
            string.append(sent + " ")
        return "".join(string).rstrip(" ")
