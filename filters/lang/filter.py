from typing import List
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from langid.langid import LanguageIdentifier, model


class LanguageFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ['af', 'am', 'an', 'ar', 'as', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de',
                 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'ga', 'gl', 'gu', 'he', 'hi',
                 'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky',
                 'la', 'lb', 'lo', 'lt', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'nb', 'ne', 'nl', 'nn',
                 'no', 'oc', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'ro', 'ru', 'rw', 'se', 'si', 'sk', 'sl', 'sq',
                 'sr', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'ug', 'uk', 'ur', 'vi', 'vo', 'wa', 'xh', 'zh',
                 'zu']

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
