import re, glob, string, os
import numpy as np
import pandas as pd
from scipy import spatial
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import spacy
import lemminflect
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

nlp = spacy.load("en_core_web_sm") 
module_use = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3")


def get_vocab(bookpath):
    ''' gets vocabulary from a book '''
    with open(bookpath) as f:
        text = f.read()
    pgext = text.split('PROJECT GUTENBERG EBOOK')
    if len(pgext)==3:
        text = pgext[1]
    text = re.sub('\W',' ',text)
    text = text.lower().replace('\n',' ')
    vocab = list(set(text.split())-set('_'))
    vocab = [x.replace('_','') for x in vocab]
    return vocab

def encode(wordlist):
    ''' makes word vectors from list '''
    return module_use.signatures["question_encoder"](
    tf.constant(wordlist))["outputs"]

def make_kdtree(vocab):
    ''' creates kdtree for fast nn search '''
    vectors = encode(vocab)
    df = pd.DataFrame(np.array(vectors),index=vocab)
    kdtree = spatial.cKDTree(df)
    return kdtree

WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'
punctuation =  string.punctuation+ ' '+'-'+'–'
pos_map = {'VERB': 'v', 'ADJ': 'a', 'ADV': 'r', 'NOUN': 'n'}

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


def tense_check(inputted, suggested):
    ''' preserves word tense '''
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

def punct_preserve(inputted):
    ''' preserves punctuation '''
    s = ''
    e = ''
    for i in inputted:
        if i in punctuation:
            s += i
        else:
            break
    
    for i in reversed(inputted):
        if i in punctuation:
            e += i
        else:
            break
            
    return (s, inputted[len(s):len(inputted)-len(e)], e[::-1])

def case_match(inputted, suggested):
    ''' preserves word case '''
    if inputted[0].isupper() and inputted[1:].islower():
        return suggested.title()
    elif inputted.isupper():
        return suggested.upper()
    else:
        return suggested.lower()

# takes string input, explore preparsing text
def grammarize(inputted, suggested):
    ''' preserves grammar of original word in restricted vocabulary '''
    target = suggested
    start_punct, original_word, end_punct = punct_preserve(inputted)
    
    if original_word == '':
        return inputted
    
    suggested = nlp(suggested)[0]
    inputted = nlp(original_word)[0]

    if inputted.pos_ == 'PROPN':
        target = inputted.text
    else:
        target = tense_check(inputted, suggested)

    target=case_match(original_word, target)
    return start_punct+target+end_punct

def normalize(word,vocab,tree):
    ''' restricts a single word to a vocabulary '''
    gord = ''.join(re.findall('[a-z]',word.lower()))
    if gord in vocab or "'" in word:
        return word
    else:
        v = encode(word)
        nn = tree.query(v,1)[-1][0]
        nearest_word = vocab[nn]
        return nearest_word

def normalize_sentence(sentence,vocab,tree):
    ''' restricts all words in a sentence to a vocabulary'''
    words = sentence.split()
    target_words = [normalize(word,vocab,tree) for word in words]
    restricted_sentence = ' '.join([t if t==w else grammarize(w, t)
                         for t,w in zip(target_words,words)])   
    return restricted_sentence
    
class VocabRestrictor(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    '''
    restricts text to vocabulary in a given book
    '''
    
    def __init__(self,bookpath='transformations/vocab_restrictor/books'):
        self.vocabs = [get_vocab(b) for b in glob.glob(bookpath+'/*')]
        self.kdtrees = [make_kdtree(v) for v in self.vocabs]
        self.books = [b.replace(bookpath+'/','').replace('.txt','')
                      for b in glob.glob(bookpath+'/*')]
        
    def generate(self,sentence: str):
        # restricts text
        restricted_sentences = [normalize_sentence(sentence,v,t)
                                for v,t in zip(self.vocabs,self.kdtrees)]
        return restricted_sentences

