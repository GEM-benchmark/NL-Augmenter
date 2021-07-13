import json
import os
import sys
import nltk

from TestRunner import convert_to_snake_case
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import wptools
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def get_cd(phrase):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    so = wptools.page(phrase, silent=True).get_parse()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    a = so.data["parsetree"]
    short_desc = BeautifulSoup(a, 'html.parser').find('title').nextSibling.contents[1].contents[0]
    return short_desc


def stop_word_removal(text_all, cached_stop_words):
    new_text_all = []
    for text in text_all:
        text1 = ' '.join([word for word in text.split() if word not in cached_stop_words])
        new_text_all.append(text1)
    return new_text_all


def get_grams(sentence, N):
    all_grams = []
    for l in range(1, N + 1):
        grams = [" ".join(sentence[i:i + l]) for i in range(len(sentence) - l + 1)]
        all_grams = all_grams + grams
    return all_grams


def prep_sent(sentence, n, cached_stop_words):
    list1 = list(set(stop_word_removal(get_grams(sentence.split(), n), cached_stop_words)))
    list1 = list(filter(None, list1))
    list1 = list(sorted(list1, key=len))[::-1]
    return list1


def get_noun_definitions(inp_sent, cached_stop_words):
    max_ngrams = 3
    inp_sent = inp_sent.lower()
    tokens = nltk.word_tokenize(inp_sent)
    pos_tagged = nltk.pos_tag(tokens)

    non_noun_tuples = list(filter(lambda x: x[1][0] != 'N', pos_tagged))
    non_nouns = [a_tuple[0] for a_tuple in non_noun_tuples]

    mentions = prep_sent(inp_sent, max_ngrams, cached_stop_words)
    mentions_dict = {}
    done_grams = non_nouns
    for men in mentions:
        if men in done_grams:
            continue
        val = None
        try:
            val = get_cd(men)
        except:
            continue
        if val is not None:
            mentions_dict[men] = val
            all_to_stop = get_grams(men.split(), len(men.split()))
            done_grams = done_grams + all_to_stop
    for key_phrase, phrase_definition in mentions_dict.items():
        if len(phrase_definition.split()) == 1:
            continue
        inp_sent = inp_sent.replace(key_phrase, key_phrase + "(" + phrase_definition.lower() + ")")
    return (inp_sent)

'''
search for noun phrases from wikidata lookup 
and then add definitions in braces after 
phrase occurences to add more context
NOTE: requires three nltk downloads (only 1 time)
'''
class AddNounDefinition(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        super().__init__(seed, max_outputs=max_outputs)
        self.cached_stop_words = stopwords.words("english")

    def generate(self, sentence: str):
        extended_text = get_noun_definitions(sentence, self.cached_stop_words)
        res_data = [extended_text]
        return res_data

'''
if __name__ == '__main__':

    tf = AddNounDefinition()

    test_cases = []
    all_sents = ["Andrew finally returned the Comic book to Chris that I bought last week",
                 "Chris borrowed the Comic book from Andrew last weekend",
                 "Turn off the light please",
                 "I love cat",
                 "Thomas loves to cook chicken every Monday", "John killed Mary with a gun"]
    for sentence in all_sents:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)
'''

