from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp
from spacytextblob.spacytextblob import SpacyTextBlob
import spacy


class TextRetainsPolarity(SentencePairOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, diff_allowed: float = 0.5):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        if "spacytextblob" not in self.nlp.pipe_names:
            self.nlp.add_pipe("spacytextblob")
        self.diff_allowed = diff_allowed

    def filter(self, sentence1: str = None, sentence2: str = None) -> bool:
        text1 = self.nlp(sentence1, disable=["parser", "tagger", "ner", 'lemmatizer'])
        text2 = self.nlp(sentence2, disable=["parser", "tagger", "ner", 'lemmatizer'])
        if abs(text1._.polarity - text2._.polarity) <= self.diff_allowed:
            return True
        else:
            return False
