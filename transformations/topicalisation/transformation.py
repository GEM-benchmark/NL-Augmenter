from initialize import spacy_nlp

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from spacy.tokens.doc import Doc

from optional import Optional

import spacy
import warnings

from transformations.topicalisation.topicalisation_utils import get_dobj_of_verb, get_prep_pobj_of_verb, \
    has_child_of_type, has_parent_of_type, get_tokens_of_pos_type, check_if_any_parent_has


def not_topicalized(object, verb):
    return object[0].idx > verb.idx


def get_object_phrase(root_token):
    # first check if the main verb's dobj is there, then take it
    object_phrase = get_dobj_of_verb(root_token)
    if object_phrase.is_present():
        return object_phrase
    # then check if prep-pobj of the main verb is there, then take the pobj
    prep_phrase = get_prep_pobj_of_verb(root_token)
    if prep_phrase.is_present():
        return prep_phrase

    # If the main verb has another 'acomp'- ed verb like "tried to eat", "failed to eat", then take the objects of that verb
    xcomp = has_child_of_type(root_token, ['xcomp', 'ccomp', 'acomp'])
    if xcomp.is_present():
        object_phrase = get_dobj_of_verb(xcomp.get())
        if object_phrase.is_present():
            return object_phrase
        prep_phrase = get_prep_pobj_of_verb(xcomp.get())
        if prep_phrase.is_present():
            return prep_phrase
    return Optional.empty()


def topicalize(original, to_move: [], verb):
    if has_parent_of_type(verb, ["conj", "cc"]):
        return topicalize_before_verb(original, to_move, verb)
    topicalized = [(" ".join([n.text for n in to_move.copy()]).capitalize())]
    for token in original:
        if token not in to_move:
            topicalized.append(token.text)
    return " ".join(topicalized).strip()


def topicalize_before_verb(original, to_move: [], verb):
    before_verb = [token for token in original if token not in list(verb.subtree) and token.pos_ is not "PUNCT"]
    topicalized = [token.text for token in before_verb]
    topicalized.append(" ".join([n.text for n in to_move.copy()]).capitalize())
    topicalized.append(", ")
    for token in original:
        if token not in to_move and token not in before_verb:
            topicalized.append(token.text)
    return " ".join(topicalized).strip()


class Topicalisation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, verbose=False):
        super().__init__(seed, verbose=verbose)
        self.seed = seed
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        if self.verbose:
            print(f"\nOriginal:  {sentence}")
        parses = self.nlp(sentence)
        return self.generateFromParse(parses)

    def generateFromParse(self, parses: Doc):
        pass
        # (1) get adjuncts
        # (2) get arguments (only those which have determiners)
        #  - not possible out of a subject argument
        #  - not possible out of an adjunct clause
        #  - not possible out of a complex NP
        generations = []
        sentences = list(parses.sents)
        if len(sentences) > 1 and self.verbose:
            warnings.warn("Seems there are more than 1 sentences - Only the first sentence would be topicalized.")
        for parse in sentences:
            verbs_and_adjs = get_tokens_of_pos_type(parse, ["VERB", "ADJ"])
            if len(
                    verbs_and_adjs) < 4:  # This is only restricted to sentences with 1 or 2 verbs, else performance drops.
                for verb in verbs_and_adjs:
                    if self.verbose:
                        print(f"VERB: {verb}")
                    object_phrase_opt = get_object_phrase(verb)
                    if object_phrase_opt.is_present() and not_topicalized(object_phrase_opt.get(),
                                                                          verb) and check_if_any_parent_has(verb,
                                                                                                            ["nsubj"]):
                        topicalized = topicalize(parse, object_phrase_opt.get(), verb)
                        if self.verbose:
                            print(f"Topicalised: {topicalized}")
                        generations.append(topicalized)
        return generations
