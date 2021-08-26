
import re 
import gensim.downloader
import inflect 
import spacy
from typing import List , Tuple
import numpy as np

import toolz
from more_itertools import partition
import logging

p = inflect.engine()
# taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py

def replace_word_in_sentence(sentence, word_to_replace, replacement):
    """
    Replace a word in a sentence with a replacement.
    """
    return re.sub(word_to_replace, replacement, sentence)

def get_nouns(sentence, nlp):
    """ given a sentence, return all the singular/plural nouns in 2 lists

    Args:
        sentence ([type]): sentence
        nlp ([spacy.lang]): spacy nlp object
    Returns:
        [tuple]: singular nouns, plural nouns
    """
    doc = nlp(sentence)

    nouns = toolz.curried.filter(lambda token: token.pos_ == "NOUN" , doc)
    # get plurals and singulars (singulars have tag "NN" plurals have tag "NNS")
    plurals, singulars = toolz.pipe( partition(lambda token : token.tag_ == "NN", nouns),
            toolz.curried.map(list))
    
    return list(map(str, singulars)), list(map(str, plurals)) 

def x_ify(word:str, wv, addition: Tuple[str, np.ndarray]) -> List:
    """
    take a word, and x-word vector to it, return the most similar word    
    Args:
        word ([str]): word
        wv ([gensim.models.keyedvectors.KeyedVectors]): word2vec gensim model
        addition ([Tuple]): (word-string, np.ndarray of the word2vec vector)
    """

    try:
        word_vec = wv[word]
    except KeyError as e:
        print(f"exception {e}, with word {word}")
        return word     
    addition_name, addition_wv = addition
    similar_words = wv.most_similar(positive=[ word_vec + addition_wv],  topn = 4)
    return [word_tup[0] for word_tup in similar_words if word_tup[0] not in (addition_name, word) ]

def man_ify(word, wv):
    """ take a word, and "man" vector to it, return the most similar word"""
    add_man_vectors= x_ify(word, wv, ('man', wv['man']))
    return add_man_vectors[:1][0] # take the top word

def woman_ify(word, wv):
    """ take a word, and "woman" vector to it, return the most similar word"""    
    add_woman_vectors = x_ify(word, wv, ('woman',wv['woman']))
    return add_woman_vectors[:1][0] # take the top word
    
def load():
    nlp = spacy.load("en_core_web_sm")
    wv = gensim.downloader.load('word2vec-google-news-300')
    return wv, nlp 

def genderify_sentence(sentence:str, wv, nlp) -> List[str]:
    """take a sentence and return a list of sentences with each proper noun replaced

    Args:
        sentence ([str]): sentence
        wv ([gensim.models.keyedvectors.KeyedVectors]): word2vec gensim model
        nlp ([spacy.lang]): spacy nlp object
    """
    sentences = []
    singulars, plurals = get_nouns(sentence, nlp)

    for noun in singulars:
        noun = str(noun)
        man_replace = man_ify(noun, wv)
        logging.debug(f"we are replacing {noun} with {man_replace}")
        sentences.append(replace_word_in_sentence(sentence, noun, man_replace ))
    
    for noun in plurals:
        noun = str(noun)
        # use the singular form
        singularized_noun = p.singular_noun(noun)
        man_replace = man_ify(singularized_noun, wv)
        #woman_replace = woman_ify(noun, wv)
        # convert the word to the plural form
        man_replace = p.plural(man_replace)
        logging.debug(f"we are replacing {noun} with {man_replace}")
        sentences.append(replace_word_in_sentence(sentence, noun, man_replace ))
    
    return sentences 

if __name__ == "__main__":
    wv, nlp = load()
    text = ("When Sebastian Thrun started working on self-driving cars at "
            "Google in 2007, few people outside of the company took him "
            "seriously. I can tell you very senior CEOs of major American "
            "car companies would shake my hand and turn away because I wasn’t "
            "worth talking to,” said Thrun, in an interview with Recode earlier "
            "this week.")
    
    doc = nlp(text)
    
    for sent in doc.sents:
        print(sent)
        gender_benders = genderify_sentence(str(sent), wv, nlp)
        for gender_bender in gender_benders:
            print("\t" + gender_bender)

