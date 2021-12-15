import spacy

from common.initialize import spacy_nlp
from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType


class TextRetainsPolarity(SentencePairOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self, strict_polarity: bool = False, diff_allowed: float = 0.5
    ):
        """
        Args:
            strict_polarity: if any change of polarity is not allowed (True)
            diff_allowed: how much of the difference between scores of two sentences is allowed
        """
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        if "spacytextblob" not in self.nlp.pipe_names:
            self.nlp.add_pipe("spacytextblob")
        self.strict_polarity = strict_polarity
        self.diff_allowed = diff_allowed

    def filter(self, sentence1: str = None, sentence2: str = None) -> bool:
        """
        Filters out sentences with not allowed polarity change.

        Args:
            sentence1: first sentence
            sentence2: second sentence

        Returns:
            boolean if transformation passes filtration
        """
        text1 = self.nlp(
            sentence1, disable=["parser", "tagger", "ner", "lemmatizer"]
        )
        text2 = self.nlp(
            sentence2, disable=["parser", "tagger", "ner", "lemmatizer"]
        )
        if self.strict_polarity:
            return True if text1._.polarity * text2._.polarity >= 0 else False
        else:
            return (
                True
                if abs(text1._.polarity - text2._.polarity)
                <= self.diff_allowed
                else False
            )
