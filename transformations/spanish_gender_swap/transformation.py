import random

import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from .gender_agreement import (
    adjective_male_to_female,
    change_participle,
    check_change_verb,
    country_gender_names,
    function_m2f,
    m2f_adjectives_animate_only,
    m2f_nouns,
    male2country,
    path_to_word_exists,
    unambiguous_pronouns,
)


def spanish_gender_swap(text, swap_names, seed=0, nlp=None):
    """Swap the gender of all gender-bearing nouns to female."""

    random.seed(seed)
    doc = nlp(text)
    r = get_replacements(doc, m2f_nouns, swap_names)
    new_toks = [
        r[ii] + tok.whitespace_ if ii in r else tok.text + tok.whitespace_
        for ii, tok in enumerate(doc)
    ]
    return ["".join(new_toks)]


def modifiable_non_noun(token):
    word = token.text.lower()
    return token.pos_ not in ["NOUN", "PROPN"] or word in unambiguous_pronouns


def get_replacements(doc, m2f_nouns, swap_names, debug=False):
    """Replace all nouns and pronouns whose gender can be swapped, and then
    swap all other words (adjectives, determiners, prepositions, participles)
    associated with them.

    If swap_names is True, also swap given names with names of another gender.
    """

    replacements = {}

    for token in doc:
        # If swap_names is True, see if we can swap names.
        if swap_names and token.pos_ == "PROPN" and token.text in male2country:
            country = random.choice(male2country[token.text])
            new_name = random.choice(country_gender_names[country]["F"])
            replacements[token.i] = new_name

        # See if we can swap the gender of nouns and pronouns.
        if (
            token.pos_ in ["NOUN", "PROPN", "PRON"]
            and token.text.lower() in m2f_nouns
        ):
            new_noun = m2f_nouns[token.text.lower()]
            if token.text[0].isupper():
                new_noun = new_noun.capitalize()
            replacements[token.i] = new_noun

    modified_tokens = [doc[ii] for ii in replacements]

    for modified_token in modified_tokens:

        # See if we can swap the gender of any of the noun's children.
        children = [c for c in modified_token.children]
        for c in children:
            if (
                modifiable_non_noun(c)
                and c.i not in replacements
                and c.pos_ in ["DET", "PRON", "ADP", "ADJ"]
            ):
                replacements[c.i] = swap_gender_of_word(c.text, c.pos_)
                if debug:
                    print("-------------------")
                    print("child added:", c.text, c.pos_, c.dep_)
                    print(
                        "child of token:", modified_token, modified_token.dep_
                    )

        # See if we can swap the gender of the noun's head.
        head = modified_token.head
        if modifiable_non_noun(head) and head.i not in replacements:
            # If the head is a verb, check to see if it is a participle
            # whose gender should agree with the noun.
            if check_change_verb(head, doc, replacements):
                replacements[head.i] = change_participle(head.text)
            elif (
                head.pos_ == "ADJ" and modified_token.dep_ != "nmod"
            ) or head.pos_ in ["DET", "PRON", "ADP"]:
                #  NOTE: prevent nmod to avoid cases like "lo bueno de mi primo."
                replacements[head.i] = swap_gender_of_word(
                    head.text, head.pos_
                )
            else:
                pass
            if debug:
                print("-------------------")
                print("head added:", head.text, head.pos_, head.dep_)
                print("head of token:", modified_token, modified_token.dep_)

    replacements = fix_remaining(doc, replacements)
    return replacements


def fix_remaining(doc, replacements, debug=False):
    """
    This function is used to do another pass over the sentence in order to:

    (1.) change the gender of other words, e.g., those connected by conjunctions
    ("italiano y rubio") or determiners ("el otro").
    (2.) modify any other adjectives which weren't changed previously due
    to incorrect POS tags or dependency parse. This only affects adjectives
    that are used to refer only to animate nouns.
    """

    for token in doc:
        if (
            token.pos_ in ["DET", "PRON", "ADP", "ADJ"]
            and token.i not in replacements
            and path_to_word_exists(token, replacements)
        ):
            replacements[token.i] = swap_gender_of_word(token.text, token.pos_)
            if debug:
                print("-------------------")
                print("head2: ", token.head.text, token.head.pos_)
                print("token:", token, token.dep_)

    # This shouldn't be necessary, but sometimes the POS tagger fails, so now
    # swap more adjectives which we know modify animate nouns.
    for token in doc:
        if (
            token.pos_ == "ADJ"
            and token.text.lower() in m2f_adjectives_animate_only
        ):
            uppercase = token.text[0].isupper()
            n = m2f_adjectives_animate_only[token.text.lower()]
            replacements[token.i] = n.capitalize() if uppercase else n

    return replacements


def swap_gender_of_word(word, pos):
    """The nouns are based on a gazetter.  But this function is used to
    change the gender of adjectives, determiners, etc.
    """

    uppercase = word[0].isupper()

    # Avoid mistakes caused by incorrect POS tags by treating
    # DET, PRON, ADP all at once.
    if pos in ["DET", "PRON", "ADP"] or word in unambiguous_pronouns:
        n = (
            function_m2f[word.lower()]
            if word.lower() in function_m2f
            else word.lower()
        )
    elif pos == "ADJ":
        n = adjective_male_to_female(word.lower())
    else:
        raise ValueError("This is a verb.")

    if uppercase:
        n = n.capitalize()

    return n


class SpanishGenderSwap(SentenceOperation):
    """Swaps all gendered nouns (and any other associated words, in order to
    maintain grammatical agreement) to their female counterparts.

    Args:
        swap_names: Also swap person names? Defaults: False.
        seed: initial seed. Defaults: 0.
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["es"]
    keywords = [
        "morphological",
        "rule-based",
        "parser-based",
        "high-precision",
        "high-coverage",
    ]

    def __init__(self, swap_names=False, seed=0):
        super().__init__(seed)
        self.swap_names = swap_names
        self.nlp = spacy.load("es_core_news_sm")

    def generate(self, sentence: str):
        perturbed_texts = spanish_gender_swap(
            text=sentence,
            swap_names=self.swap_names,
            seed=self.seed,
            nlp=self.nlp,
        )
        return perturbed_texts
