
import re 
import gensim.downloader
import spacy
from typing import List , Tuple
import numpy as np
import datetime
import logging

# taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py

def replace_word_in_sentence(sentence, word_to_replace, replacement):
    """
    Replace a word in a sentence with a replacement.
    """
    return re.sub(word_to_replace, replacement, sentence)

def get_nouns(sentence, nlp):
    """
    Get the nouns in a sentence.
    """
    doc = nlp(sentence)
    return [token.text for token in doc if token.pos_ == "NOUN"] 
    # altertatively:
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
                chunk.root.head.text)
    print("---")
    for chunk in doc.noun_chunks:
        print(chunk.root.text)

def x_ify(word, wv, addition: Tuple[str, np.ndarray]) -> List :

    try:
        word_vec = wv[word]
    except KeyError:
        return word     
    addition_name, addition_wv = addition
    breakpoint()
    similar_words = wv.most_similar(positive=[ word_vec + addition_wv],  topn = 4)
    return [word_tup[0] for word_tup in similar_words if word_tup[0] not in (addition_name, word) ]

def man_ify(word, wv):
    return x_ify(word, wv, ('man', wv['man']))

def woman_ify(word, wv):
    return x_ify(word, wv, ('woman',wv['woman']))

def load():
    start = datetime.datetime.now()

    logging.debug("load spacy models")
    nlp = spacy.load("en_core_web_sm")
    now = datetime.datetime.now()
    logging.debug(f"time to run : {now - start}")

    logging.debug("load word2vec model")
    wv = gensim.downloader.load('word2vec-google-news-300')
    now = datetime.datetime.now()
    logging.debug(f"time from start : {now - start}")
    start = now

    start = now
    return wv, nlp 

if __name__ == "__main__":
    wv, nlp = load()

    print(man_ify("queen", wv))
    print(man_ify("king", wv ))


if False:

    nlp = spacy.load("en_core_web_sm")
    text = ("When Sebastian Thrun started working on self-driving cars at "
            "Google in 2007, few people outside of the company took him "
            "seriously. “I can tell you very senior CEOs of major American "
            "car companies would shake my hand and turn away because I wasn’t "
            "worth talking to,” said Thrun, in an interview with Recode earlier "
            "this week.")

    doc = nlp(text)

    print([chunk for chunk in doc])


    doc = nlp("Autonomous cars shift insurance liability toward manufacturers")

    for sent in doc.sents:
        nouns = get_nouns(sent.text)
