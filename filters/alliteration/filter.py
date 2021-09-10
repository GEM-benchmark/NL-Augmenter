import string

import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class Alliteration(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["morphological"]

    def __init__(self, stopwords: bool = True):
        super().__init__()
        self.stopwords = stopwords
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None, min_sentence_length=3) -> bool:
        def get_phonemes(word: str):
            # We are adding some digraphs to avoid 'sand' and 'shady' to alliterate.
            # Then we check for these digraphs first
            digraphs = ["ch", "ph", "sh", "th"]
            if word[:2] in digraphs:
                return word[:2]
            else:
                return word[:1]

        # If the input contains multiple sentences, only take the first sentence that has the min_sentence_length
        sent = self.nlp(sentence.lstrip())
        segmented_sentence = list(sent.sents)
        for k in segmented_sentence:
            # Skip any too short 'sentences' that contain no alphanumeric characters
            if len(k.text) > min_sentence_length and k.text.lower().islower():
                first_sentence = k.text
                break

        # Convert to lower, remove punctuation, tokenize into words
        sentenceS = (
            first_sentence.lower()
            .translate(str.maketrans("", "", string.punctuation))
            .split()
        )

        # if self.stopwords: # This somehow does not work, it always returns interfaces.SentenceOperation.SentenceOperation, even with a getter method
        if self.stopwords:
            if not set(sentenceS).issubset(self.nlp.Defaults.stop_words):
                all_stopwords = self.nlp.Defaults.stop_words
                # Remove all stopwords from our sentence
                sentenceS = [
                    word for word in sentenceS if word not in all_stopwords
                ]

        # tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        # tokenizedB = [token.text for token in tokenized if token.text.isalpha()]
        # tokened_text = [w.lower() for w in tokenizedB]  # make it lowercase

        first_phon = get_phonemes(sentenceS[0])
        start_phon = [get_phonemes(word) == first_phon for word in sentenceS]

        return all(start_phon)


# Alliteration(SentenceOperation).filter("It is I in it.")
# Alliteration(SentenceOperation).filter("It is not my fault.")
# print(Alliteration(SentenceOperation).filter("She showed Shawn shady shandy. This is the second sentence."))
# print(Alliteration(SentenceOperation).filter("She showed Shawn some shady shandy."))
# print(Alliteration(SentenceOperation).filter("Peter Piper picked a peck of pickled peppers."))
