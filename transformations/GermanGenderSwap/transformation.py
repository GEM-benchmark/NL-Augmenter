# -*- coding: utf-8 -*-
import random
import string
from typing import List
from checklist.editor import Editor
from interfaces.SentenceOperation import SentenceOperation
from evaluation.evaluation_engine import evaluate, execute_model
from tasks.TaskTypes import TaskType
import json

with open("data.json", "r", encoding="utf-8") as f:
    names = json.load(f)

with open("noun_pairs.json", "r", encoding="utf-8") as fn:
    nouns = json.load(fn)

f = list(names["1"].values())
m = list(names["2"].values())

# Noun Pairs.
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


def replace_prev_word(ind, text, noundict):
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
            newtext = replace_name_in_list(ind, text, nouns)
            newtext = replace_prev_word(ind, newtext, preceeding_word)

        else:
            newtext = text
    newtext = " ".join(str(x) for x in newtext)
    return newtext


# Personal Pronouns.
personalp = {
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


def replace_name_in_list(ind, text, noundict):
    t2 = text
    for i in ind:
        t2[i] = noundict[t2[i]]
    return t2


def replace_personal(inp, personalp):
    i = replace_punc(inp)
    text = i.split()
    for name in personalp.keys():
        if name in text:
            ind = get_index(text, name)
            newtext = replace_name_in_list(ind, text, personalp)
        else:
            newtext = text
    newtext = " ".join(str(x) for x in newtext)
    return newtext


def findname(sent, malenames, femalenames):
    t = sent.split()
    for word in t:
        if word in malenames:
            w = word
            return w
        elif word in femalenames:
            w = word
            return w
        else:
            print(" ")


def swapname(name, names):
    for n in names["2"].values():
        if name in m:
            new = random.choice([i for i in names["1"].values()])
            return new
        else:
            return name


def newnamerep(m, f, inp, names):
    n = findname(inp, m, f)
    sent = inp
    t = sent.split()
    for word in t:
        if word in m and n != "None":
            if n != None:
                fname = swapname(word, names)
                sent = sent.replace(word, str(fname))
            else:
                sent = sent
    return sent


def german_nouns(inp, nouns, names):
    text = replace_punc(inp)
    t1 = replace_noun_pairs(text, nouns)
    t2 = replace_personal(t1, personalp)
    t3 = newnamerep(m, f, t2, names)
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
