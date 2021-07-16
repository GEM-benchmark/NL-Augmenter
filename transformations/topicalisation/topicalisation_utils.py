from optional import Optional
from spacy.tokens.doc import Doc


def has_parent_of_type(node, types: list):
    return node.dep_ in types


def check_if_any_parent_has(node, types: list):
    if has_child_of_type(node, types):
        return True
    parent = list(node.ancestors)
    if len(parent) == 0:
        return False
    else:
        return check_if_any_parent_has(parent[0], types)  # parent[0] since it's a dep tree


def has_child_of_type(node, types: list):
    for child in node.children:
        if child.dep_ in types:
            return Optional.of(child)
    return Optional.empty()


def get_tokens_of_pos_type(sentence, types: list):
    for token in sentence:
        if token.pos_ in types:
            yield token


def get_children_of_dep_type(verb, types: list):
    for token in verb.children:
        if token.dep_ in types:
            yield token


"""
Gets the node and all the elements in the subtree (children as well as their children and so on)
"""


def get_node_and_all_children(node):
    s = []
    for child in node.subtree:
        s.append(child)
    return s


"""
Gets the node and only it's immediate children. 
"""


def get_node_and_children(node):
    s = []
    for child in node.children:
        s.append(child)
    return s


"""
I ate those burgers --> those burgers
I described such scenarios --> such scenarios
"""


def get_dobj_of_verb(verb):
    for child in verb.children:
        # Get the direct object - only if it has a determiner/a-mod
        # Also to allow direct objects which have prep as a child. - "Shelly has indeed uncovered [part of our plan.]"
        if (child.dep_ in ['dobj', 'npadvmod']) and has_child_of_type(child,
                                                                      ["det", "amod", "prep", "nummod"]).is_present():
            object_phrase = get_node_and_all_children(child)
            return Optional.of(object_phrase)
    return Optional.empty()


"""
I am terrified of those burgers --> those burgers
"""


def get_prep_pobj_of_verb(verb):
    for child in verb.children:
        # Get the prep object - only if it has a determiner/a-mod
        if (child.dep_ in ['prep']):
            pobj = has_child_of_type(child, ["pobj"])
            if pobj.is_present() and has_child_of_type(pobj.get(), ["det", "amod", "nummod"]).is_present():
                object_phrase = get_node_and_all_children(pobj.get())
                return Optional.of(object_phrase)
    return Optional.empty()


def prep_phrase(node):
    pp = has_child_of_type(node, ["prep", "prt"])
    if pp.is_present():
        pp_nodes = get_node_and_all_children(pp.get())
        return Optional.of(pp_nodes)
    return Optional.empty()


import string


def movePunctuation(se):
    for c in string.punctuation:
        se = se.replace(" " + c, "")
    return se


class SyntacticVariation(object):

    def generate(self, sentence: str):
        pass

    def generateFromParse(self, parse: Doc):
        pass

    def name(self):
        return self.__class__.__name__
