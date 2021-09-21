import random
import re

import coreferee
import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp

"""
Randomizes names in text for a 50/50 gender breakdown. Handles pronouns.
"""

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
    if pronoun_text == 'himself':
        return 'herself'
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
    
    if pronoun_text == 'herself':
        return 'himself'
    
    return None
def make_name_map(parsed_text, male_names, female_names):
        """
        Identifies person names in text and creates mapping to a random name (50/50 chance of male vs. female)
        """
        name_map = {}
        for ent in parsed_text.ents:
            if ent.label_ == "PERSON":
                name_map[ent.text] = randomize_gender(
                    male_names, female_names
                )
        return name_map

def swap(text, name_map):
    """
    Replaces names with matched names
    """
    for old_name, new_name in name_map.items():
        text = re.sub(r"\b%s\b" % old_name, new_name[1], text)
    return text

def pronoun_fix(text, parsed_text, name_map):
    """
    Fixes pronouns to match new names
    """
    pronouns = ["she", "her", "hers", "he", "his", "him", "himself", "herself"]
    pronoun_dicts = {"male": female_to_male, "female": male_to_female}

    new_text = ""
    i = 0

    for tok in parsed_text:

        if tok.text.lower() in pronouns:
            ref = parsed_text._.coref_chains.resolve(tok)
#             print(tok, ref, tok.tag_, tok.pos_)
            if ref is None or len(ref) > 1:
                continue

            else:
                name_options = [
                    key for key in name_map if ref[0].text in key
                ]
                if len(name_options) == 1:
                    gender = name_map[name_options[0]][0]
                    replacer = pronoun_dicts[gender](tok)

                    if replacer:
                        replacer = case_match(tok.text, replacer)
                        new_text += text[i : tok.idx]
                        new_text += replacer
                        i = tok.idx + len(tok.text)

    new_text += text[i : len(text)]
    return new_text  

def run_swap(sentence, seed=42, nlp=None, male_names=None, female_names=None):
    """
    Runs pronoun fix and name swaps to generate new text
    """
    random.seed(seed)
    text = sentence
    parsed_text = nlp(sentence)
    name_map = make_name_map(parsed_text, male_names, female_names)
    text = pronoun_fix(text, parsed_text, name_map)
    text = swap(text, name_map)
    return text

class GenderRandomizer(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["lexical", "model-based", "rule-based", "named entity recognition", "coreference resolution"]

    def __init__(self, seed=42, max_outputs=1):
        
        super().__init__(seed)
        self.max_outputs = max_outputs
        # These lists are from https://www.kaggle.com/nltkdata/names
        with open(
            "transformations/gender_randomizer/names/female.txt"
        ) as female:
            self.female_names = [
                name.strip("\n") for name in female.readlines()
            ]
        with open("transformations/gender_randomizer/names/male.txt") as male:
            self.male_names = [name.strip("\n") for name in male.readlines()]

        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm", disable=["lemmatizer"]) #spacy.load("en_core_web_sm", disable=["lemmatizer"])
        self.nlp.add_pipe("coreferee")


    def generate(self, sentence: str):
        """
        Returns altered text, and saves it in self.text attribute
        sentence: text to modify
        """
        gender_randomized = run_swap(sentence, seed=self.seed, nlp=self.nlp, male_names=self.male_names, female_names=self.female_names)
        return gender_randomized
