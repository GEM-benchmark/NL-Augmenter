import hashlib
import json
import os
import random
import re

import numpy as np
import spacy

from nlaugmenter.common.initialize import spacy_nlp
from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


def hash(input: str):
    t_value = input.encode("utf8")
    h = hashlib.sha256(t_value)
    n = int(h.hexdigest(), base=16)
    return n


class ChangeGenderCultureDiverseName:
    def __init__(self, data_path) -> None:

        with open(data_path, "r") as f:
            self.names = json.load(f)
        self.countries = list(self.names.keys())
        self.genders = ["M", "F"]

        self.name_all = set()
        self.name2gender = {}
        self.name2country = {}

        for country in self.names.keys():
            for gender in ["M", "F"]:
                for name in self.names[country][gender]:
                    self.name_all.add(name)

                    if name not in self.name2gender.keys():
                        self.name2gender[name] = {gender}
                    else:
                        self.name2gender[name].add(gender)

                    if name not in self.name2country.keys():
                        self.name2country[name] = {country}
                    else:
                        self.name2country[name].add(country)

        self.name_all = sorted(self.name_all)
        for name in self.name_all:
            self.name2gender[name] = sorted(self.name2gender[name])
            self.name2country[name] = sorted(self.name2country[name])

    def apply(
        self,
        doc,
        retain_gender=False,
        retain_culture=False,
        n=10,
        max_output=10,
        seed=None,
    ):
        """Replace names with another name, considering gender and cultural diversity

        Parameters
        ----------
        doc : spacy.token.Doc
            input
        retain_gender: bool
            sample new names with the same gender
        retain_culture: bool
            sample new names with the same culture
        n : int
            number of names to replace original names with
        max_output: int
            maximum number of perturbed sentences to output
        seed : int
            random seed

        Returns
        -------
        ret, ret_m
            ret: list
                list of perturbed sentences
            ret_m: [(old_name), (new_name),...]
                list of (old_name, new_name) pairs

        """

        if seed is not None:
            random.seed(seed)
        ents = [
            x.text
            for x in doc.ents
            if np.all([a.ent_type_ == "PERSON" for a in x])
        ]
        ret = []
        ret_m = []
        for x in ents:
            name = x.split()[0]
            capito = name[0].isupper()  # pun intended, hint: Italian
            name = name.capitalize()
            if name in self.name_all:
                gender = self.name2gender[name]
                country = self.name2country[name]
                if retain_gender:
                    gender_choose_from = gender
                else:
                    gender_choose_from = self.genders
                if retain_culture:
                    country_choose_from = country
                else:
                    country_choose_from = self.countries

                new_countries = random.choices(country_choose_from, k=n)
                new_genders = random.choices(gender_choose_from, k=n)
                new_names = [
                    random.choice(self.names[c][n])
                    for c, n in zip(new_countries, new_genders)
                ]
                if not capito:
                    new_names = [n.lower() for n in new_names]

                for new_name in new_names:
                    ret.append(
                        re.sub(r"\b%s\b" % re.escape(name), new_name, doc.text)
                    )
                    ret_m.append((name, new_name))

        if len(ret) > max_output:
            idxs = random.choices(range(len(ret)), k=max_output)
            return [ret[idx] for idx in idxs], [ret_m[idx] for idx in idxs]
        else:
            return ret, ret_m


class GenderCultureDiverseName(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "el",
        "sr",
        "ja",
        "lt",
        "en",
        "ar",
        "sa",
        "ta",
        "te",
        "rw",
        "ff",
        "ro",
        "zh",
        "es",
        "fa",
        "hy",
        "hi",
        "ak",
        "mk",
        "is",
        "st",
        "xh",
        "pt",
        "sv",
        "fr",
        "az",
        "mi",
        "af",
        "ko",
        "gu",
        "de",
        "kk",
        "mt",
        "zu",
        "nn",
        "tl",
        "be",
        "so",
        "pl",
        "ca",
        "da",
        "bn",
        "rn",
        "ns",
        "nb",
        "tt",
        "kn",
        "ti",
        "ha",
        "eu",
        "tr",
        "si",
        "pa",
        "sw",
        "sl",
        "bg",
        "lv",
        "hr",
        "uk",
        "mr",
        "sk",
        "ps",
        "bs",
        "se",
        "he",
        "tn",
        "it",
        "hu",
        "cs",
        "nl",
        "ru",
        "et",
        "uz",
        "gl",
        "sq",
        "ee",
        "fi",
        "cy",
    ]
    # language code following ISO 639-1 standard
    keywords = [
        "lexical",
        "noise",
        "rule-based",
        "external-knowledge-based",
        "high-coverage",
        "high-precision",
        "social-reasoning",
        "world-knowledge",
    ]

    def __init__(
        self,
        n=1,
        seed=0,
        max_output=1,
        retain_gender=False,
        retain_culture=False,
        data_path=None,
    ):
        super().__init__(seed)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.n = n
        self.max_output = max_output

        if data_path is None:
            self.changer = ChangeGenderCultureDiverseName(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "data.json"
                ),
            )
        else:
            self.changer = ChangeGenderCultureDiverseName(
                data_path,
            )

    def generate(
        self,
        sentence: str,
        retain_gender: bool = False,
        retain_culture: bool = False,
    ):
        seed = (
            self.seed + hash(sentence) + retain_gender * 1 + retain_culture * 2
        )
        perturbed_texts, _ = self.changer.apply(
            self.nlp(sentence),
            retain_gender,
            retain_culture,
            self.n,
            self.max_output,
            seed,
        )

        return perturbed_texts


"""
if __name__ == '__main__':
    import itertools
    test = GenderCultureDiverseName()

    sentences = [
        'Rachel Green, a sheltered but friendly woman, flees her wedding day and wealthy yet unfulfilling life.',
        'Phoebe Buffay is an eccentric masseuse and musician.',
        'Joey has many short-term girlfriends.',
        'Chandler Bing is a sarcastic and self-deprecating IT manager.',
        'Monica was overweight as a child.']
    outputs = []
    for s in sentences:
        for retain_gender, retain_culture in itertools.product([False, True], [False, True]):
            inputs = {
                "sentence": s,
                "retain_gender": retain_gender,
                "retain_culture": retain_culture
            }
            p = test.generate(**inputs)
            outputs.append([s, retain_gender, retain_culture, p])
"""
