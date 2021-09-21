from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp
import spacy


class TextContainsKeywordsFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords=None):
        super().__init__()
        if keywords is None:
            keywords = ["these", "keywords", "are", "only", "for", "demo"]
        self.key_words = keywords
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None) -> bool:
        tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        tokenized = [token.text for token in tokenized]
        contained_keywords = set(tokenized).intersection(set(self.key_words))
        return bool(contained_keywords)
