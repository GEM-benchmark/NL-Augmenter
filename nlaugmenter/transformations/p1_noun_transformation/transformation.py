# import os
# import sys
#
# import nltk
# import wptools
# from bs4 import BeautifulSoup
# from nltk.corpus import stopwords
#
# from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
# from nlaugmenter.tasks.TaskTypes import TaskType
#
# """
# Base Class for implementing the different input transformations a generation should be robust against.
# """
#
#
# def get_cd(phrase):
#     """
#     Returns a definition for noun phrase
#     Keyword arguments:
#     phrase -- phrase (str)
#     """
#     sys.stdout = open(os.devnull, "w")
#     sys.stderr = open(os.devnull, "w")
#     so = wptools.page(phrase, silent=True).get_parse()
#     sys.stdout = sys.__stdout__
#     sys.stderr = sys.__stderr__
#     a = so.data["parsetree"]
#     short_desc = (
#         BeautifulSoup(a, "html.parser")
#         .find("title")
#         .nextSibling.contents[1]
#         .contents[0]
#     )
#     return short_desc
#
#
# def stop_word_removal(text_all, cached_stop_words):
#     """
#     Returns text with removed stop words
#     Keyword arguments:
#     text_all -- list of all texts (list of str)
#     cached_stop_words -- list of all stopwords (list of str)
#     """
#     new_text_all = []
#     for text in text_all:
#         text1 = " ".join(
#             [word for word in text.split() if word not in cached_stop_words]
#         )
#         new_text_all.append(text1)
#     return new_text_all
#
#
# def get_grams(sentence, n):
#     """
#     Returns phrases i.e. windowed sub
#     strings with range (1-N) window
#     Keyword arguments:
#     sentence -- utterance  (str)
#     n -- max_ngram (int)
#     """
#     all_grams = []
#     for index in range(1, n + 1):
#         grams = [
#             " ".join(sentence[i : i + index])
#             for i in range(len(sentence) - index + 1)
#         ]
#         all_grams = all_grams + grams
#     return all_grams
#
#
# def prep_sent(sentence, n, cached_stop_words):
#     """
#     Returns preprocessed n grams of sentence
#     Keyword arguments:
#     sentence -- utterance  (str)
#     n -- max_ngram (int)
#     cached_stop_words -- list of all stopwords (list of str)
#     """
#     clean_list = list(
#         set(
#             stop_word_removal(
#                 get_grams(sentence.split(), n), cached_stop_words
#             )
#         )
#     )
#     clean_list = list(filter(None, clean_list))
#     clean_list = list(sorted(clean_list, key=len))[::-1]
#     return clean_list
#
#
# def get_noun_definitions(inp_sent, cached_stop_words, max_ngrams):
#     """
#     Returns sentence with added noun
#     definitions in braces, appended post
#     original noun phrase.
#     Keyword arguments:
#     inp_sent -- utterance  (str)
#     cached_stop_words -- list of all stopwords (list of str)
#     max_ngrams -- max_ngram (int)
#     """
#     tokens = nltk.word_tokenize(inp_sent)
#     pos_tagged = nltk.pos_tag(tokens)
#
#     non_noun_tuples = list(filter(lambda x: x[1][0] != "N", pos_tagged))
#     non_nouns = [a_tuple[0] for a_tuple in non_noun_tuples]
#
#     mentions = prep_sent(inp_sent, max_ngrams, cached_stop_words)
#     mentions_dict = {}
#     done_grams = non_nouns
#     for men in mentions:
#         if men in done_grams:
#             continue
#         try:
#             val = get_cd(men)
#         except Exception:
#             continue
#         if val is not None:
#             mentions_dict[men] = val
#             all_to_stop = get_grams(men.split(), len(men.split()))
#             done_grams = done_grams + all_to_stop
#     for key_phrase, phrase_definition in mentions_dict.items():
#         if len(phrase_definition.split()) == 1:
#             continue
#         inp_sent = inp_sent.replace(
#             key_phrase, key_phrase + "(" + phrase_definition.lower() + ")"
#         )
#     return inp_sent
#
#
# """
# search for noun phrases from wikidata lookup
# and then add definitions in braces after
# phrase occurrences to add more context
# NOTE: requires three nltk downloads (only 1 time)
# """
#
#
# class AddNounDefinition(SentenceOperation):
#     tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
#     languages = ["en"]
#     heavy = True
#
#     def __init__(self, seed=0, max_outputs=1):
#         nltk.download("stopwords")
#         nltk.download("punkt")
#         nltk.download("averaged_perceptron_tagger")
#         super().__init__(seed, max_outputs=max_outputs)
#         self.cached_stop_words = stopwords.words("english")
#         self.max_ngrams = 3
#
#     def generate(self, sentence: str):
#         extended_text = get_noun_definitions(
#             sentence, self.cached_stop_words, self.max_ngrams
#         )
#         res_data = [extended_text]
#         return res_data
#
#
# """
# if __name__ == '__main__':
#
#     tf = AddNounDefinition()
#
#     test_cases = []
#     all_sents = ["Andrew finally returned the Comic book to Chris that I bought last week",
#                  "Chris borrowed the Comic book from Andrew last weekend",
#                  "Turn off the light please",
#                  "I love cat",
#                  "Thomas loves to cook chicken every Monday", "John killed Mary with a gun"]
#     for sentence in all_sents:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
#         )
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json_file)
#     with open('test.json', 'w', encoding='utf-8') as f:
#         json.dump(json_file, f, ensure_ascii=False, indent=2)
# """
