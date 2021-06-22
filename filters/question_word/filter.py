from tasks.TaskTypes import TaskType
from typing import List
from interfaces.SentenceOperation import SentenceOperation
import spacy


class KeywordsFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords: List[str] = []):
        super().__init__()
        self.keywords = keywords
        self.nlp = spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None) -> bool:
        tokenized = self.nlp(sentence, disable=["parser", "tagger", "ner"])
        tokenized = [token.text.lower() for token in tokenized]
        contained_keywords = set(tokenized).intersection(set(self.keywords))
        return bool(contained_keywords)


class WhereQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["where"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)


class WhatQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["what"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)


class WhoQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["who"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)


class WhichQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["which"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)


class WhyQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["why"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)


class WhenQuestion(KeywordsFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["when"]):
        super().__init__(keywords=keywords)

    def filter(self, sentence: str) -> bool:
        return super().filter(sentence=sentence)
