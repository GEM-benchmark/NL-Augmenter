"""
Base Class for implementing the different input transformations 
a generation should be robust against.
"""

import logging
import re
from typing import Callable, List, Tuple

import gensim.downloader
import inflect
import numpy as np
import spacy
import toolz
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def _load() -> Tuple:
    """helper function which loads spacy and gensim models

    Returns:
        [Tuple]: gensim model (loaded from word2vec-google-news-300), spacy model (en_core_web_sm)
    """
    logging.debug("loading spacy model")
    nlp = spacy.load("en_core_web_sm")
    logging.debug("loading gensim model")
    wv = gensim.downloader.load('word2vec-google-news-300')
    return wv, nlp


def replace_word_in_sentence(sentence, word_to_replace, replacement):
    """
    Replace a word in a sentence with a replacement.
    """
    return re.sub(word_to_replace, replacement, sentence)


def get_nouns(sentence: str, nlp) -> List:
    """ given a sentence, return all the singular/plural nouns in 2 lists

    Args:
        sentence ([type]): sentence
        nlp ([spacy.lang]): spacy nlp object
    Returns:
        [list]: list of nouns in the sentence
    """
    # get all the nouns from the sentence
    return list(
        map(
            str,  # convert spacy.tokens to strings
            toolz.filter(
                lambda token: token.pos_ == "NOUN",  # get all the nouns
                nlp(sentence))))


def x_ify(word: str,
          wv,
          x: Tuple[str, np.ndarray],
          inflect_engine,
          banned_words=None) -> str:
    """
    take a word, and x-word vector to it, return the most similar word    
    Args:
        word ([str]): word
        wv ([gensim.models.keyedvectors.KeyedVectors]): word2vec gensim model
        addition ([Tuple]): (word-string, np.ndarray of the word2vec vector)
    Returns:
        [str]: most similar word to word + addition_word
    """
    x_name, x_wv = x
    try:
        word_vec = wv[word]
    except KeyError as e:
        print(f"exception {e}, with word {word}")
        return word

    similar_words = wv.most_similar(positive=[word_vec + x_wv], topn=10)

    # compile all the words to ignore
    banned_words = banned_words or []
    banned_words += [x_name, word]
    banned_words = banned_words + [
        inflect_engine.plural(word) for word in banned_words
    ]
    banned_words = [word.lower() for word in banned_words]

    similar_words = [
        word_tup[0] for word_tup in similar_words
        if word_tup[0].lower() not in banned_words
    ]
    return similar_words[:1][0]  # take only the top word


def _is_capitalized(word: str) -> bool:
    return word[0].isupper()


def _capitalize(word):
    return word[0].upper() + word[1:]


def swap_out_words(sentence: str, noun: str, x_ify_function: Callable[[str],
                                                                      str],
                   inflect_engine) -> str:
    """ given a sentence and a noun, return a sentence that replaces the noun 
    with something transformed through the x_ify_function
    (i.e. man-ify would add the man-vector to the word, and return the closest word)
    Example:
        swap_out_words("The knight fought the King.", "King" , woman_ify_function) ->
            -> "the knight fought the queen"

    Args:
        sentence (str): original sentence
        noun (str): noun to x-ify + replace
        is_plural (bool): is the original noun a plural noun
        x_ify_function (Callable[[str], str]): transformation function that converts noun into noun + word-vector, and returns the closest word to that new vector
            i.e. "woman" + "king" = "queen"

    Returns:
        str: sentence that has noun replaced with x-ified version of itself
    """
    # use the singular form of the noun
    # inflect has a strange interface - if word is singular,returns False, if plural, returns singular-noun (str)
    is_singular_noun = not bool(inflect_engine.singular_noun(noun))
    singularized_noun = inflect_engine.singular_noun(
        noun) if not is_singular_noun else noun

    # find the replacement word for the noun
    replacement = x_ify_function(singularized_noun.lower())
    # copy the same capitalization as the original noun
    replacement = _capitalize(replacement) if _is_capitalized(
        noun) else replacement
    # some words from w2v come out with _, ie. "brain_plasticity", split them apart
    split_words = replacement.split("_")
    print(
        f"replacing {noun} with {replacement}. and split words are {split_words}"
    )
    # if the noun is a plural one, convert the words to the plural form
    if not is_singular_noun:
        # in english typically only the last word in a compound noun is pluralized
        split_words[-1] = inflect_engine.plural(split_words[-1])
    replacement = " ".join(split_words)
    logging.debug(f"we are replacing {noun} with {replacement}")

    return replace_word_in_sentence(sentence, noun, replacement)


def generate_sentences(sentence: str, max_outputs: int, wv, nlp,
                       inflect_engine) -> List[str]:
    """take a sentence and return a list of sentences with each proper noun replaced

    Args:
        sentence ([str]): sentence
        max_outputs (int) : max sentences to return
        wv ([gensim.models.keyedvectors.KeyedVectors]): word2vec gensim model
        nlp ([spacy.lang]): spacy nlp object
        inflect_engine : engine from inflect module that allows easy pluralization and singularization
    
    Returns:
        [list]: list of sentences with each noun replaced with a male-ify + a woman-ified version
    """
    nouns = get_nouns(sentence, nlp)
    banned_words = ["man", "woman", "men", "women", "boy", "girl"]
    manify_function = lambda word: x_ify(word=word,
                                         wv=wv,
                                         x=('man', wv['man']),
                                         inflect_engine=inflect_engine,
                                         banned_words=banned_words)
    womanify_function = lambda word: x_ify(word=word,
                                           wv=wv,
                                           x=('woman', wv['woman']),
                                           inflect_engine=inflect_engine,
                                           banned_words=banned_words)
    swapped_sentences = []
    count = 0
    for noun in nouns:
        if noun.lower(
        ) in banned_words:  # ignore replacing man/woman with itself
            continue
        swapped_sentences.append(
            swap_out_words(sentence, str(noun), manify_function,
                           inflect_engine))
        count += 1
        swapped_sentences.append(
            swap_out_words(sentence, str(noun), womanify_function,
                           inflect_engine))
        count += 1
        if count > max_outputs:
            break
    if count == 0:
        return [sentence]
    return swapped_sentences[:max_outputs]


class GenderifyOperation(SentenceOperation):
    """ Apply man-vector + woman-vector to each of the nouns in the sentence"""
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.inflect_engine = inflect.engine()

        self.word2vec, self.nlp = _load()

    def generate(self, sentence: str):

        return generate_sentences(sentence=sentence,
                                  wv=self.word2vec,
                                  nlp=self.nlp,
                                  max_outputs=self.max_outputs,
                                  inflect_engine=self.inflect_engine)


'''

# Used for compiling test.json
if __name__ == "__main__":
    wv, nlp = _load()
    sentences = [
        "Andrew finally returned the French book to Chris that I bought last week",
        "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
        "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
        "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."
    ]
    inflect_engine = inflect.engine()

    import json
    for sentence in sentences:
        d = {
            "class":
            "GenderifyOperation",
            "inputs": {
                "sentence": sentence
            },
            "outputs": [{
                "sentence":
                generate_sentences(sentence=sentence,
                                   max_outputs=1,
                                   wv=wv,
                                   nlp=nlp,
                                   inflect_engine=inflect_engine)[0]
            }]
        }

        print(json.dumps(d))
        print(",")
'''
