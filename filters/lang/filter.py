from typing import List
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from langid.langid import LanguageIdentifier, model


class LanguageFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, lang: List[str] = None, min_prob: float = 0.5):
        super().__init__()
        if lang is None:
            lang = ['en']
        self.lang = lang
        self.min_prob = min_prob

    def filter(self, sentence: str = None) -> bool:
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        lang, prob = identifier.classify(sentence)
        for match_lang in self.lang:
            if match_lang == lang and self.min_prob <= prob:
                return True
        return False
