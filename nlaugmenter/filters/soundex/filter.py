import jellyfish
import spacy

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.utils.initialize import spacy_nlp


class PhoneticMatchFilter(SentenceOperation):
    tasks = [e for e in TaskType]
    languages = ["en"]

    def __init__(self, keywords, algorithm: str = "soundex"):
        super().__init__()
        self.key_words = keywords
        try:
            self.algo = getattr(jellyfish, algorithm)
        except AttributeError:
            raise NotImplementedError(
                "Jellyfish does not implement `{}`".format(algorithm)
            )
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None) -> bool:
        tokenized = self.nlp(
            sentence, disable=["parser", "tagger", "ner", "lemmatizer"]
        )
        phonetic = [self.algo(token.text) for token in tokenized]
        matchers = [self.algo(kw) for kw in self.key_words]
        contains_soundalikes = set(phonetic).intersection(set(matchers))
        return bool(contains_soundalikes)
