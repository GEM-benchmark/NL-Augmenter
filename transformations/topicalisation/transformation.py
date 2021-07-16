import itertools
import random
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
    topicalized = [("".join([n.string for n in to_move.copy()]).capitalize())]
    topicalized.append(", ")
    for token in original:
        if token not in to_move:
            topicalized.append(token.string)
    return "".join(topicalized).strip()


def topicalize_before_verb(original, to_move: [], verb):
    before_verb = [token for token in original if token not in list(verb.subtree) and token.pos_ is not "PUNCT"]
    topicalized = [token.string for token in before_verb]
    topicalized.append("".join([n.string for n in to_move.copy()]).capitalize())
    topicalized.append(", ")
    for token in original:
        if token not in to_move and token not in before_verb:
            topicalized.append(token.string)
    return "".join(topicalized).strip()


class Topicalisation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
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
            for verb in get_tokens_of_pos_type(parse, ["VERB", "ADJ"]):
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


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = ButterFingersPerturbation(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
