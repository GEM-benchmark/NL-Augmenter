import numpy as np
import spacy

from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType

import os
import re
import json
import random
import hashlib
from checklist.perturb import process_ret


def hash(input:str):
    t_value = input.encode('utf8')
    h = hashlib.sha256(t_value)
    n = int(h.hexdigest(),base=16)
    return n

class change_gender_culture_diverse_name_two_way:
    def __init__(self, data_path, retain_gender=False, retain_culture=False) -> None:

        self.retain_gender = retain_gender
        self.retain_culture = retain_culture
        with open(data_path, 'r') as f:
            self.names = json.load(f)
        self.countries = list(self.names.keys())
        self.genders = ['M', 'F']

        self.name_all = set()
        self.name2gender = {}
        self.name2country = {}

        for country in self.names.keys():
            for gender in ['M', 'F']:
                for name in self.names[country][gender]:
                    self.name_all.add(name)

                    if name not in self.name2gender.keys():
                        self.name2gender[name] = set([gender])
                    else:
                        self.name2gender[name].add(gender)
                    
                    if name not in self.name2country.keys():
                        self.name2country[name] = set([country])
                    else:
                        self.name2country[name].add(country)

    def apply(self, doc, tar, n=10, max_output=10, seed=None):
        """Replace names with another name, considering gender and cultural diversity

        Parameters
        ----------
        doc : spacy.token.Doc
            input
        meta : bool
            if True, will return list of (orig_name, new_name) as meta
        n : int
            number of names to replace original names with
        seed : int
            random seed

        Returns
        -------
        list(str)
            if meta=True, returns (list(str), list(tuple))
            Strings with names replaced.

        """

        if seed is not None:
            random.seed(seed)
        ents = [x.text for x in doc.ents if np.all([a.ent_type_ == 'PERSON' for a in x])]
        ret_s = []
        ret_t = []
        ret_m = []
        for x in ents:
            name = x.split()[0]
            capito = name[0].isupper() # pun intended, hint: Italian
            name = name.capitalize()
            if name in self.name_all:
                gender = self.name2gender[name]
                country = self.name2country[name]
                if self.retain_gender:
                    gender_choose_from = gender
                else:
                    gender_choose_from = self.genders
                if self.retain_culture:
                    country_choose_from = country
                else:
                    country_choose_from = self.countries
            
                new_countries = random.choices(country_choose_from, k=n)
                new_genders = random.choices(gender_choose_from, k=n)
                new_names = [random.choice(self.names[c][n]) for c,n in zip(new_countries, new_genders)]
                if not capito:
                    new_names = [n.lower() for n in new_names]
                
                for new_name in new_names:
                    ret_s.append(re.sub(r'\b%s\b' % re.escape(name), new_name, doc.text))
                    ret_t.append(re.sub(r'\b%s\b' % re.escape(name), new_name, tar))
                    ret_m.append((name, new_name))
        
        if len(ret_s) > max_output:
            idxs = random.choices(range(len(ret_s)), k=max_output)
            return [ret_s[idx] for idx in idxs], [ret_t[idx] for idx in idxs], [ret_m[idx] for idx in idxs]
        else:
            return ret_s, ret_t, ret_m
                


class gender_culture_diverse_name_two_way(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    tgt_languages = ['en']

    def __init__(self, n=1, seed=0, max_output=1, retain_gender=False, retain_culture=False, data_path=None):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n
        self.max_output = max_output

        if data_path is None:
            self.changer = change_gender_culture_diverse_name_two_way(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json'),
                retain_gender, 
                retain_culture
            )
        else:
            self.changer = change_gender_culture_diverse_name_two_way(
                data_path,
                retain_gender, 
                retain_culture
            )

    def generate(self, sentence: str, target: str):
        random.seed(self.seed + hash(sentence))
        perturbed_source, perturbed_target, _ = self.changer.apply(self.nlp(sentence), target, self.n, self.max_output)

        return [(perturbed_source, perturbed_target)]

from TestRunner import convert_to_snake_case
tf = gender_culture_diverse_name_two_way()
src = ["Andrew finally returned the French book to Chris that I bought last week",
           "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate"
           " to indicate the relation between two or more arguments."]
tgt = ["Andrew did not return the French book to Chris that was bought earlier",
           "Gapped sentences such as Paul likes coffee and Mary tea, lack an overt predicate!", ]

test_cases = []
for idx, (sentence, target) in enumerate(zip(src, tgt)):
        perturbeds = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": []}
        )
        for sentence, target in perturbeds:
            test_cases[idx]["outputs"].append({"sentence": sentence, "target": target})

A = 1