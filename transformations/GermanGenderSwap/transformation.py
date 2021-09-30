# -*- coding: utf-8 -*-


noun_pairs = {
    "Arzt": "Arztin",
    "Bruder": "Schwester",
    "Prinz": "Prinzessin",
    "Vater": "Mutter",
    "Stiefsohn": "Stieftochter",
    "Herzog": "Herzogin",
    "Zauberer": "Hexe",
    "Baron": "Baronin",
    "Prinz": "Prinzessin",
    "Schwiegersohn": "Schwiegersohn",
    "Freund": "Freundin ",
    "Onkel": "Tante ",
    "Jager": "Jagerin",
    "Meister": "Herrin",
    "Grossvater": "Oma",
    "Madchen": "Junge",
    "Mann": "Frau",
    "Priester": "Priesterin",
    "Monch": "Nonne",
    "Gott": " Gottin",
    "Steward": "Sewardess",
    "Mord": "Morderin",
    "Kellner": "Kellnerin",
    "Kaiser": "Kaiserin",
    "Konig": "Konigin",
    "Ehemann": "Frau",
    "Stiefvater": "Stiefmutter",
    "Sohn": "Tochter",
    "Geschaftsmann": "Geschaftsfrau",
    "Witwer": "Witwe",
    "Schauspieler": "Schauspielerin",
    "Krankenpfleger": "Krankenschwester",
    "Schreiber": "Schreiberin",
    "Patensohn": "Patentochter",
    "Pate": "Patin",
    "Techniker": "Technikerin",
    "Ingenieur": "Ingenieurin ",
    "Fahrer": "Fahrerin",
    "Chirurg": "Chirurgin",
    "Mechaniker": "Mechanikerin",
    "Pionier": "Pionierin",
    "Regisseur": "Regisseurin",
    "Karikaturist": "Karikaturistin",
    "Musiker": "Musikerin",
    "Physiker": "Physikerin",
    "Grunder": "Grunderin",
    "Muslim": "Muslimin",
    "Christ": "Christin",
    "Jude": "Judin",
    "Atheist": "Atheistin",
    "Botaniker": "Botanikerin",
    "Chemiker": "Chemikerin",
    "Historiker": "Historikerin",
    "Burger": "Burgerin",
    "Gegner": "Gegnerin",
    "Auslander": "Auslanderin",
    "Sanger": "Sangerin",
    "Dichter": "Dichterin",
    "Teilnehmer": "Teilnehmerin",
    "Handwerker": "Handwerkerin",
    "Partisan": "Partisanin",
    "Soldat": "Soldatin",
    "Boss": "Bossin",
    "Chef": "Chefin",
    "Fuhrer": "Fuhrerin",
    "Kommandant": "Kommandantin",
    "Kapitan": "Kapitanin",
    "Sklave": "Sklavin",
    "Entertainer": "Entertainerin",
    "Prasident": "Prasidentin",
    "Skifahrer": "Skifahrerin",
    "Fussballer": "Fussballerin",
    "Cricketspieler": "Cricketspielerin",
    "Berater": "Beraterin",
    "Therapeut": "Therapeutin",
    "Psychologe": "Psychologin",
    "Kardiologe": "Kardiologin",
    "Dermatologe": "Dermatologin",
    "Zahnarzt": "Zahnarztin",
    "Praktiker": "Praktikerin",
    "Neurologe": "Neurologin",
    "Ernahrungsberater": "Ernahrungsberaterin",
    "Anasthesist": "Anasthesistin",
    "Apotheker": "Apothekerin",
    "Chirurg": "Chirurgin",
    "Entbindungspfleger": "Hebamme",
    "Audiologe": "Audiologin",
    "Augenoptiker": "Augenoptikerinnen",
    "Optiker": "Optikerin",
    "Tierarzte": "Tierarztinnen",
    "Podologen": "Podologinnen",
    "Endokrinologe": "Endokrinologin",
    "Geriater": "Geriater",
    "Internist": "Internistin",
    "Geburtshelfer": "Geburtshelferin",
    "Urologe": "Urologin",
    "Neurochirurg": "Neurochirurgin",
    "Statistiker": "Statistikerin",
    "Wissenschaftler": "Wissenschaftlerin",
    "Erfinder": "Erfinderin",
    "Urheber": "Urheberin",
    "Autor": "Autorin",
    "Herrscher": "Herrscherin",
    "Schriftsteller": "Schriftstellerin",
    "Archaologe": "Archaologin",
    "Astronaut": "Astronautin",
    "Astronom": "Astronomin",
    "Biochemiker": "Biochemikerin",
    "Gynakologe": "Gynakologin",
    "Okologe": "Okologin",
    "Förster": "Försterin",
    "Aufseher": "Aufseherin",
    "Geograph": "Geographin",
    "Naturforscher": "Naturforscherin",
    "Pathologe": "Pathologin",
    "Palaontologe": "Palaontologin",
    "Anthropologe": "Anthropologin",
    "Okonom": "Okonomin",
    "Historiker": "Historikerin",
    "Soziologe": "Soziologin",
    "Planer": "Planerin",
    "Klempner": "Klempnerin",
    "Schweisser": "Schweisserin",
    "Holzarbeiter": "Holzarbeiterinnen",
    "Arbeiter": "Arbeiterin",
    "Muller": "Mullerin",
    "Leibwachter": "Leibwachterin",
    "Polizist": "Polizistin",
    "Rechtsanwalt": "Rechtsanwaltin",
    "Stellvertreter": "Stellvertreterin",
    "Vertreter": "Vertreterin",
    "Verkaufer": "Verkauferin",
    "Verkaufer": "Verkauferin",
    "Aufseher": "Aufseherin",
    "Rektor": "Rektorin",
    "Pastor": "Pastorin",
    "Cousin": "Cousine",
    "Tanzer": "Tanzerin",
    "Dieb": "Diebin",
    "Ehepartner": "Ehepartnerin",
    "Illustrator": "Illustratorin",
    "Designer": "Designerin",
    "Jager": "Jagerin",
    "Angreifer": "Angreiferin",
    "Uberlebender": "Uberlebende",
    "Einwohner": "Einwohnerin",
    "Bewohner": "Bewohnerin",
    "Forscher": "Forscherin",
    "Programmierer": "Programmiererin",
    "Professor": "Professorin",
    "Dozent": "Dozentin",
    "Begleiter": "Begleiterin",
    "Besucher": "Besucherin",
    "Theologe": "Theologin",
    "Immigrant": "Immigrantin",
    "Farmer": "Farmerin",
    "Senator": "Senatorin",
    "Wanderer": "Wanderin",
    "Kurator": "Kuratorin",
    "Wachter": "Wachterin",
    "Treuhander": "Treuhanderin",
    "Huter": "Huterin",
    "Spion": "Spionin",
    "Klager": "Klagerin",
    "Antragsteller": "Antragstellerin",
    "Dieb": "Diebin",
    "Pazifist": "Pazifistin",
    "Metzger": "Metzgerin",
    "Verfuhrer": "Verfihrerin",
    "Kanzler": "Kanzlerin",
    "Gewinner": "Gewinnerin",
    "Einsiedler": "Einsiedlerin",
    "Prostituierter": "Prostituierte",
    "Gastronom": "Gastronomin",
    "Laufer": "Lauferin",
    "Bote": "Botin",
    "Journalist": "Journalistin",
    "Publizist": "Publizistin",
    "Vegetarier": "Vegetarierin",
    "Schwimmer": "Schwimmerin",
    "Uhrmacher": "Uhrmacherin",
    "Lugner": "Lugnerin",
    "Schwindler": "Schwindlerin",
    "Stripper": "Stripperin",
    "Maler": "Malerin",
    "Richter": "Richterin",
    "Experte": "Expertin",
    "Komponist": "Komponistin",
    "Trainer": "Trainerin",
    "Tutor": "Tutorin",
    "Erzieher": "Erzieherin",
    "Chiropraktiker": "Chiropraktikerin",
    "Blogger": "Bloggerin",
    "Aktivist": "Aktivistin",
    "Banker": "Bankerin",
    "Biograph": "Biographin",
    "Pilot": "Pilotin",
    "Schiedsrichter": "Schiedsrichterin",
    "Abenteurer": "Abenteurerin",
    "Schneider": "Schneiderin",
    "Ubersetzer": "Ubersetzerin",
    "Verrater": "Verraterin",
    "Sunder": "Sunderin",
    "Bildhauer": "Bildhauerin",
    "Politiker": "Politikerin",
    "Philosoph": "Philosophin",
    "Ornithologe": "Ornithologin",
    "Motorradfahrer": "Motorradfahrerin",
    "Radfahrer": "Radfahrerin",
    "Moderator": "Moderatorin",
    "Missionar": "Missionarin",
    "Kuppler": "Kupplerin",
    "Mikrobiologe": "Mikrobiologin",
    "Holzfaller": "Holzfallerin",
    "Interviewer": "Interviewerin",
    "Zigeuner": "Zigeunerin",
    "Gitarrist": "Gitarristin",
    "Wahrsager": "Wahrsagerin",
    "Fischhandler": "Fischhandlerin",
    "Taucher": "Taucherin",
    "Springer": "Springerin",
    "Diplomat": "Diplomatin",
    "Stellvertreter": "Stellvertreterin",
    "Masseur": "Masseuse",
    "Neffe": "Nichte",
    "Lowe": "Lowin",
    "Kater": "Katze",
}

# -*- coding: utf-8 -*-
import random
import string
from typing import List
from checklist.editor import Editor
from interfaces.SentenceOperation import SentenceOperation
from evaluation.evaluation_engine import evaluate, execute_model
from tasks.TaskTypes import TaskType
import json

f = open(
    "data.json",
)
names = json.load(f)
f = list(names["1"].values())
m = list(names["2"].values())

# Noun Pairs
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


def replace_noun_pairs(inp, noun_pairs):
    i = replace_punc(inp)
    text = i.split()
    for name in noun_pairs.keys():
        if name in text:
            ind = get_index(text, name)
            newtext = replace_name_in_list(ind, text, noun_pairs)
            newtext = replace_prev_word(ind, newtext, preceeding_word)
        else:
            newtext = text
    newtext = " ".join(str(x) for x in newtext)
    return newtext


# Personal Pronouns
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


# Replace Names
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


def german_nouns(inp, noun_pairs):
    text = replace_punc(inp)
    t1 = replace_noun_pairs(text, noun_pairs)
    t2 = replace_personal(t1, personalp)
    t3 = newnamerep(m, f, t2, names)
    t4 = restore_punc(t3)
    return t4


class GermanGenderSwap(SentenceOperation):

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["de"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs)
        self.noun_pairs = noun_pairs

    def generate(self, sentence: str):
        return [german_nouns(sentence, self.noun_pairs)]


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = GermanGenderSwap(max_outputs=1)
    test_cases = []
    for sentence in [
        "Mein Vater und dein Bruder sind hier?",
        "Er ist der Prasident, sie ist die Herrscherin und sie werden jetzt bald Ehemann und Ehefrau sein!",
        "Er ist ein Arzt und mein Vater.",
        "Ich sehe, dass der Dichter und die Schauspielerin jetzt Freunde sind!",
    ]:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    print(json.dumps(json_file, indent=2))
