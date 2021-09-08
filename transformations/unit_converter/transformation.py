import itertools
import json
import os
import random

import spacy
from num2words import num2words
from word2number import w2n

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def convert(text, X, units, plurals, converter):
    is_word, not_zero = False, False
    if str(X.root) in units:  # check if the unit is supported
        q = str(X.text).replace(str(X.root), "")  # q is the number of units
        try:
            q = float(q)
        except ValueError:
            q = w2n.word_to_num(
                q
            )  # if it is not a numerical value, convert it and remember to convert it back after unit conversion
            is_word = True
        q /= converter[
            plurals[X.root.lemma_]
        ]  # convert to base unit (meters, kilograms)
        new_unit = random.choice(
            units
        )  # pick a random new unit from the available one (the original one is included)
        while not not_zero:
            if new_unit in plurals:
                new_unit = plurals[new_unit]  # set to plural form
            q_new = (
                q * converter[new_unit]
            )  # convert from base unit to new unit
            q_new = float("{:.3f}".format(q_new))  # clean format
            if q_new != 0:
                not_zero = True
                q = q_new
            else:  # it happens if the conversion is not optimal (e.g., we avoid to convert 1 centimeter to kilometers)
                new_unit = random.choice(units)

        if (
            int(q) == 1 and q - int(q) < 0.01
        ):  # if the converted number of units is 1, put to singular
            new_unit = list(plurals.keys())[
                list(plurals.values()).index(new_unit)
            ]

        if (
            is_word
        ):  # if the quantity was in word format, put it back to word format
            q = num2words(q).replace("-", " ")
        else:
            q = str(q)
        new_text = q + " " + new_unit
        text = text.replace(X.text, new_text)
    return text


def convert_units(self, text, seed=0, max_outputs=1):
    random.seed(seed)
    doc = self.nlp(text)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        perturbed_text = text
        for X in doc.ents:
            if X.label_ == "QUANTITY":
                perturbed_text = convert(
                    perturbed_text,
                    X,
                    self.units_lengths,
                    self.plurals_lengths,
                    self.converter_lengths,
                )
                perturbed_text = convert(
                    perturbed_text,
                    X,
                    self.units_weights,
                    self.plurals_weights,
                    self.converter_weights,
                )
        perturbed_texts.append(perturbed_text)

    return perturbed_texts


class UnitConverter(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

        converter_plurals_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "converter_plurals.json",
        )

        d = json.load(open(converter_plurals_path, "r"))

        self.converter_lengths = d["converter_lengths"]
        self.converter_weights = d["converter_weights"]
        self.plurals_lengths = d["plurals_lengths"]
        self.plurals_weights = d["plurals_weights"]

        self.units_lengths = list(self.plurals_lengths.keys()) + list(
            self.plurals_lengths.values()
        )
        self.units_weights = list(self.plurals_weights.keys()) + list(
            self.plurals_weights.values()
        )

    def generate(self, sentence: str):
        perturbed_texts = convert_units(
            self=self,
            text=sentence,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
