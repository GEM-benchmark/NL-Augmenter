import string

import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class Alliteration(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["morphological"]

    def __init__(self, stopwords: bool = True, min_alliteration_length=3):
        super().__init__()
        self.stopwords = stopwords
        self.min_alliteration_length = min_alliteration_length
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
            # We are adding some digraphs to avoid 'sand' and 'shady' to alliterate.
            # Then we check for these digraphs first
            digraphs = ["ch", "ph", "sh", "th"]
            if word[:2] in digraphs:
                return word[:2]
            else:
                return word[:1]

        def segment_sentences(sentence, min_sentence_length):
            """
            If the input contains multiple sentences, only take the sentences that have the min_sentence_length and that do contain alphanumeric characters.
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

        # tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        # tokenizedB = [token.text for token in tokenized if token.text.isalpha()]
        # tokened_text = [w.lower() for w in tokenizedB]  # make it lowercase

        # Process input sentences
        sentenceS = segment_sentences(sentence, min_sentence_length)

        # Iterate through sentences
        sentence_count = []
        for sen in sentenceS:

            first_phon = get_phonemes(sen[0])
            start_phon = [get_phonemes(word) == first_phon for word in sen]
            sentence_count.append(
                sum(start_phon) >= self.min_alliteration_length
            )

        return any(
            sentence_count
        )  # return True if any of the input sentences are alliterative


# Alliteration(SentenceOperation).filter("It is I in it.")
# Alliteration(SentenceOperation).filter("It is not my fault.")
# print(Alliteration(SentenceOperation).filter("4 *((( ::). She showed Aquarium Shawn shady shandy. This is the second sentence Sandy sorted. It is imminent in Iowa."))
# print(Alliteration(SentenceOperation).filter("She showed Shawn some shady shandy."))
# print(Alliteration(SentenceOperation).filter("Peter Piper picked a peck of pickled peppers."))
