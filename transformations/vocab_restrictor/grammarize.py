import spacy
import pattern3
import re
import lemminflect
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
nlp = spacy.load("en_core_web_sm")


WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

def preserve_pos(word, from_pos, to_pos):
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])

    # return all the possibilities sorted by probability
    return result


pos_map = {'VERB': 'v', 'ADJ': 'a', 'ADV': 'r', 'NOUN': 'n'}
def tense_check(inputted, suggested):
    if inputted.lemma_ == suggested.lemma_:
        return inputted.text

    elif (inputted.pos_ != suggested.pos_) and inputted.pos_ in pos_map and suggested.pos_ in pos_map:
        possibilities = preserve_pos(suggested.text, pos_map[suggested.pos_], pos_map[inputted.pos_])
        
        #inelegant
        stem = suggested.text
        stem = stem[:4]
        for possibility, prob in possibilities:
            if stem in possibility:
                suggested = nlp(possibility)[0]
                break
                
    if inputted.tag_ != suggested.tag_:
        return suggested._.inflect(inputted.tag_)

    return suggested.text

def case_match(inputted, suggested):
    if inputted.islower():
        return suggested.lower()
    elif inputted.isupper():
        return suggested.upper()
    else:
        return inputted

# takes string input, explore preparsing text
def grammarize(inputted, suggested, unparsed = True):
    
    if unparsed:
        original_word = inputted
        target = suggested

        inputted = nlp(inputted)[0]
        suggested = nlp(suggested)[0]
    else:
        original_word = inputted.text
        target = suggested.text

    if inputted.pos_ == 'PROPN':
        target = inputted.text
    else:
        target = tense_check(inputted, suggested)

    return case_match(original_word, target)
