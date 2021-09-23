#!/usr/bin/env python3
# *_* coding: utf-8 *_*

import string

import numpy as np
import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class Alliteration(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["morphological"]

    def __init__(
        self,
        stopwords: bool = True,
        min_alliteration_length: int = 3,
        allowed_offwords: int = 2,
    ):
        super().__init__()
        self.stopwords = stopwords
        self.min_alliteration_length = min_alliteration_length
        self.allowed_offwords = allowed_offwords
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None, min_sentence_length=3) -> bool:
        """
        This filter returns True if any of the input sentences is an alliteration.
        A sentence is deemed an alliteration if it contains a minimum alliteration length of (Default) 3.
        These alliterative words do not need to appear contiguously.
        This means that e.g. "Peter Aquarium prepared a pepperoni pizza." is an alliteration
        as it contains more than 3 alliterative non-stopword words (despite "Aquarium").
        By default, stop words are removed and do not count to the alliteration.
        """

        def get_phonemes(word: str):
            """
            We are adding some digraphs to avoid 'sand' and 'shady' to alliterate.
            Then we check for these digraphs first
            """
            digraphs = ["ch", "ph", "sh", "th"]
            if word[:2] in digraphs:
                return word[:2]
            else:
                return word[:1]

        def segment_sentences(self, sentence, min_sentence_length):
            """
            If the input contains multiple sentences, only take the sentences that have the min_sentence_length
            and that do contain alphanumeric characters.
            """
            sent = self.nlp(sentence.lstrip())
            segmented_sentence = list(sent.sents)
            all_stopwords = self.nlp.Defaults.stop_words
            filt_sentences = []
            for k in segmented_sentence:
                # Skip any too short 'sentences' that contain no alphanumeric characters
                if (
                    len(k.text) > min_sentence_length
                    and k.text.lower().islower()
                ):
                    valid_sentences = k.text
                else:
                    continue

                # Convert to lower, remove punctuation, tokenize into words
                sentenceS = (
                    valid_sentences.lower()
                    .translate(str.maketrans("", "", string.punctuation))
                    .split()
                )

                if self.stopwords:
                    if not set(sentenceS).issubset(
                        self.nlp.Defaults.stop_words
                    ):
                        # Remove all stopwords from our sentence
                        sentenceS = [
                            word
                            for word in sentenceS
                            if word not in all_stopwords
                        ]
                filt_sentences.append(sentenceS)

            return filt_sentences

        def rolling_window(data, windowlen):
            """
            Create a 1-dimensional rolling window of size windowlen.
            If the windowlen is smaller than the length of the data, use the length of the data instead.
            """
            if len(data) < windowlen:
                windowlen = len(data)
            shape = data.shape[:-1] + (
                data.shape[-1] - windowlen + 1,
                windowlen,
            )
            strides = data.strides + (data.strides[-1],)
            return np.lib.stride_tricks.as_strided(
                data, shape=shape, strides=strides
            )

        def find_contiguous_elements(
            elements, min_alliteration_length, allowed_offwords
        ):
            """
            Create rolling windows of size min_alliteration_length + allowed_offwords
            and check if any window contains a block of the same elements of the size min_alliteration_length.
            Return True if any window with the min_alliteration_length is found, False otherwise.
            """
            rolling_sent = rolling_window(
                elements, min_alliteration_length + allowed_offwords
            )

            for windows in rolling_sent:
                if (
                    windows == max(set(windows), key=sorted(windows).count)
                ).sum() >= min_alliteration_length:
                    return True

            return False

        # Process input sentences
        sentenceS = segment_sentences(self, sentence, min_sentence_length)

        # Iterate through sentences
        sentence_count = []
        for sen in sentenceS:
            cat_sentence = np.array([get_phonemes(word) for word in sen])
            phonemes_bool = find_contiguous_elements(
                cat_sentence,
                self.min_alliteration_length,
                self.allowed_offwords,
            )
            sentence_count.append(phonemes_bool)

        return any(
            sentence_count
        )  # return True if any of the input sentences are alliterative
