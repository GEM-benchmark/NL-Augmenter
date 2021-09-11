from typing import List
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from langid.langid import LanguageIdentifier, model


class LanguageFilter(SentenceOperation):
    """
    Instantiates a new language-based filter.

    Attributes
    ----------
    lang : List[str] = None
        List of search languages to match input sequences against.
    min_prob : float = 0.5
        Minimum acceptable confidence of language match.

    Methods
    -------
    filter(sentence: str = None) -> bool:
        Filter on the input sentence, returning True if classification matches any of the search languages with
        confidence above the minimum threshold.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ['af', 'am', 'an', 'ar', 'as', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de',
                 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'ga', 'gl', 'gu', 'he', 'hi',
                 'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky',
                 'la', 'lb', 'lo', 'lt', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'nb', 'ne', 'nl', 'nn',
                 'no', 'oc', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'ro', 'ru', 'rw', 'se', 'si', 'sk', 'sl', 'sq',
                 'sr', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'ug', 'uk', 'ur', 'vi', 'vo', 'wa', 'xh', 'zh',
                 'zu']
    keywords = ['model-based']

    def __init__(self, lang: List[str] = None, min_prob: float = 0.5):
        super().__init__()
        if lang is None:
            lang = ['en']
        self.lang = lang
        self.min_prob = min_prob

    def filter(self, sentence: str = None) -> bool:
        """
        Classify the language of the input sentence, then match against the list of search languages.
        @param sentence: input sequence as a string
        @return: True if input sequence language is in list of search languages, False if not
        """
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        lang, prob = identifier.classify(sentence)
        for match_lang in self.lang:
            if match_lang == lang and self.min_prob <= prob:
                return True
        return False
