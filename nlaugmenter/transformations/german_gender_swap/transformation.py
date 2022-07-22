# -*- coding: utf-8 -*-
import json
import os
import random
import string

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json"),
    "r",
    encoding="utf-8",
) as f:
    names = json.load(f)

with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "noun_pairs.json"
    ),
    "r",
    encoding="utf-8",
) as fn:
    nouns = json.load(fn)

f = list(names["1"].values())
m = list(names["2"].values())


def replace_punc(text):
    for i in string.punctuation:
        text = text.replace(i, " " + i)
    return text


def restore_punc(text):
    for i in string.punctuation:
        text = text.replace(" " + i, i)
    return text


preceeding_word = {
    "der": "die",
    "Der": "Die",
    "ein": "eine",
    "Ein": "Eine",
    "mein": "meine",
    "Mein": "Meine",
    "dein": "deine",
    "Dein": "Deine",
    "sein": "seine",
    "Sein": "Seine",
    "unser": "unsere",
    "Unser": "Unsere",
    "euer": "eure",
    "Euer": "Eure",
    "euren": "eure",
    "Euren": "Eure",
    "eurem": "eurer",
    "Eurem": "Eurer",
    "ihr": "ihre",
    "Ihr": "Ihre",
    "den": "die",
    "Den": "Die",
    "einen": "eine",
    "Einen": "Eine",
    "dieser": "diese",
    "Dieser": "Diese",
    "diesen": "diese",
    "Diesen": "Diese",
    "meinen": "meine",
    "Meinen": "Meine",
    "deinen": "deine",
    "Deinen": "Deine",
}


def replace_prev_word(ind, text, noun_dict):
    t2 = text
    for i in ind:
        prev_ind = i - 1
        if t2[prev_ind] in preceeding_word.keys():
            t2[prev_ind] = preceeding_word[t2[prev_ind]]
        else:
            t2 = text
    return t2


def replace_noun_pairs(inp, nouns):
    i = replace_punc(inp)
    text = i.split()
    for name in nouns.keys():
        if name in text:
            ind = get_index(text, name)
            new_text = replace_name_in_list(ind, text, nouns)
            new_text = replace_prev_word(ind, new_text, preceeding_word)

        else:
            new_text = text
    new_text = " ".join(str(x) for x in new_text)
    return new_text


personal_pron = {
    "er": "sie",
    "Er": "Sie",
    "ihr": "sie",
    "Ihr": "Sie",
    "ihn": "sie",
    "Ihn": "Sie",
    "Ihm": "Ihr",
    "ihm": "ihr",
}


def get_index(wl, n):
    indices = [i for i, x in enumerate(wl) if x == n]
    return indices


def replace_name_in_list(ind, text, noun_dict):
    t2 = text
    for i in ind:
        t2[i] = noun_dict[t2[i]]
    return t2


def replace_personal(inp, personal_pron):
    i = replace_punc(inp)
    text = i.split()
    for name in personal_pron.keys():
        if name in text:
            ind = get_index(text, name)
            new_text = replace_name_in_list(ind, text, personal_pron)
        else:
            new_text = text
    new_text = " ".join(str(x) for x in new_text)
    return new_text


def find_name(sent, male_names, female_names):
    t = sent.split()
    for word in t:
        if word in male_names:
            w = word
            return w
        elif word in female_names:
            w = word
            return w
        else:
            print(" ")


def swap_name(name, names):
    for n in names["2"].values():
        if name in m:
            new = random.choice([i for i in names["1"].values()])
            return new
        else:
            return name


def new_name_rep(m, f, inp, names):
    n = find_name(inp, m, f)
    sent = inp
    t = sent.split()
    for word in t:
        if word in m and n != "None":
            if n is not None:
                fname = swap_name(word, names)
                sent = sent.replace(word, str(fname))
            else:
                sent = sent
    return sent


def german_nouns(inp, nouns, names):
    text = replace_punc(inp)
    t1 = replace_noun_pairs(text, nouns)
    t2 = replace_personal(t1, personal_pron)
    t3 = new_name_rep(m, f, t2, names)
    t4 = restore_punc(t3)
    return t4


class GermanGenderSwap(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["de"]
    keywords = [
        "lexical",
        "rule-based",
        "high-coverage",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs)
        self.nouns = nouns
        self.names = names

    def generate(self, sentence: str):
        return [german_nouns(sentence, self.nouns, self.names)]
