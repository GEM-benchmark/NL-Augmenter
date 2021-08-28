import random
import re

import coreferee
import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Randomizes names in text for a 50/50 gender breakdown. Handles pronouns.
"""
nlp = spacy.load("en_core_web_sm", disable=["lemmatizer"])
nlp.add_pipe("coreferee")


def randomize_gender(male, female):
    """
    Randomly chooses between male and female names, and then randomly selects a name
    male: list of male names
    female: list of female names
    """
    gender = random.choice(["male", "female"])
    if gender == "male":
        return (gender, random.choice(male))
    elif gender == "female":
        return (gender, random.choice(female))


def case_match(inputted, suggested):
    """
    Matches case to that of original word
    inputted: original word
    suggested: word to replace original world
    """
    if inputted.islower():
        return suggested.lower()
    elif inputted.isupper():
        return suggested.upper()
    else:
        return suggested.title()


def male_to_female(pronoun):
    """
    Takes a pronoun and converts to appropriate feminine pronoun if not already masculine.
    pronoun: pronoun to convert to feminine pronoun
    """
    pronoun_text = pronoun.text.lower()
    if pronoun_text == "he":
        return "she"
    if pronoun_text == "him":
        return "her"
    if pronoun_text == "his":
        if pronoun.tag_ == "PRP":
            return "hers"
        else:
            return "her"
    return None


def female_to_male(pronoun):
    """
    Takes a pronoun and converts to appropriate masculine pronoun if not already masculine
    pronoun: pronoun to convert to masculine pronoun
    """
    pronoun_text = pronoun.text.lower()
    if pronoun_text == "she":
        return "he"
    if pronoun_text == "her":
        if pronoun.tag_ == "PRP$":
            return "his"
        else:
            return "him"
    if pronoun_text == "hers":
        return "his"

    return None


class GenderRandomizer(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):

        # These lists are from https://www.kaggle.com/nltkdata/names
        with open(
            "transformations/gender_randomizer/names/female.txt"
        ) as female:
            self.female_names = [
                name.strip("\n") for name in female.readlines()
            ]
        with open("transformations/gender_randomizer/names/male.txt") as male:
            self.male_names = [name.strip("\n") for name in male.readlines()]

        self.text = None  # holds sentence
        self.parsed = None  # holds result of spacy nlp pipeline
        self.name_map = {}  # map of names to selected names

    def make_name_map(self):
        """
        Identifies person names in text and creates mapping to a random name (50/50 chance of male vs. female)
        """
        for ent in self.parsed.ents:
            if ent.label_ == "PERSON":
                self.name_map[ent.text] = randomize_gender(
                    self.male_names, self.female_names
                )

    def swap(self):
        """
        Replaces names with matched names
        """
        for old_name, new_name in self.name_map.items():
            self.text = re.sub(r"\b%s\b" % old_name, new_name[1], self.text)

    def pronoun_fix(self):
        """
        Fixes pronouns to match new names
        """
        pronouns = ["she", "her", "hers", "he", "his", "him"]
        pronoun_dicts = {"male": female_to_male, "female": male_to_female}

        new_text = ""
        i = 0

        for tok in self.parsed:

            if tok.text.lower() in pronouns:
                ref = self.parsed._.coref_chains.resolve(tok)

                if ref is None or len(ref) > 1:
                    continue

                else:
                    name_options = [
                        key for key in self.name_map if ref[0].text in key
                    ]
                    if len(name_options) == 1:
                        gender = self.name_map[name_options[0]][0]
                        replacer = pronoun_dicts[gender](tok)

                        if replacer:
                            replacer = case_match(tok.text, replacer)
                            new_text += self.text[i : tok.idx]
                            new_text += replacer
                            i = tok.idx + len(tok.text)

        new_text += self.text[i : len(self.text)]
        self.text = new_text  # save altered text

    def run_swap(self, sentence):
        """
        Runs pronoun fix and name swaps to generate new text
        """
        self.text = sentence
        self.parsed = nlp(sentence)
        self.make_name_map()
        self.pronoun_fix()
        self.swap()
        return self.text

    def generate(self, sentence: str):
        """
        Returns altered text, and saves it in self.text attribute
        sentence: text to modify
        """
        return self.run_swap(sentence)
