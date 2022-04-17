from typing import List

import spacy

from nlaugmenter.interfaces.QuestionAnswerOperation import (
    QuestionAnswerOperation,
)
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.utils.initialize import spacy_nlp


class BaseFilter(QuestionAnswerOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, keywords: List[str] = []):
        super().__init__()
        self.question_words = keywords
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Determines if some keyword is present in the given question or not"""
        tokenized = self.nlp(question)
        tokenized = [token.text.lower() for token in tokenized]
        contained_keywords = set(tokenized).intersection(
            set(self.question_words)
        )
        return bool(contained_keywords)


class WhereQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["where"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with Where question words
        Returns bool value"""
        return super().filter(context, question, answers)


class WhatQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["what"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with What question words
        Returns bool value"""
        return super().filter(context, question, answers)


class WhoQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["who"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with Who question words
        Returns bool value"""
        return super().filter(context, question, answers)


class WhichQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["which"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with Which question words
        Returns bool value"""
        return super().filter(context, question, answers)


class WhyQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["why"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with Why question words
        Returns bool value"""
        return super().filter(context, question, answers)


class WhenQuestion(BaseFilter):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self, keywords=["when"]):
        super().__init__(keywords=keywords)

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions with When question words
        Returns bool value"""
        return super().filter(context, question, answers)


class NumericQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a numeric(non dates)
        Returns bool value"""
        for ans in answers:
            tokenized = self.nlp(ans)
            tags = [i.pos_ for i in tokenized]
            ner = [i.label_ for i in tokenized.ents]
            if "NUM" in tags and "DATE" not in ner:
                return True
        return False


class DateQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a Date
        Returns bool value"""
        for ans in answers:
            tokenized = self.nlp(ans)
            tags = [i.pos_ for i in tokenized]
            ner = [i.label_ for i in tokenized.ents]
            if "NUM" in tags and "DATE" in ner:
                return True
        return False


class PersonQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a named entity(Person)
        Returns bool value"""
        if not NumericQuestion().filter(
            context=context, question=question, answers=answers
        ):
            for ans in answers:
                tokenized = self.nlp(ans)
                ner = [i.label_ for i in tokenized.ents]
                if "PERSON" in ner:
                    return True
        return False


class LocationQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a named entity(Location)
        Returns bool value"""
        if not NumericQuestion().filter(
            context=context, question=question, answers=answers
        ):
            for ans in answers:
                tokenized = self.nlp(ans)
                ner = [i.label_ for i in tokenized.ents]
                if "LOC" in ner or "GPE" in ner:
                    return True
        return False


class CommonNounPhraseQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a common noun Phrase
        Returns bool value"""
        if not NumericQuestion().filter(
            context=context, question=question, answers=answers
        ):
            for ans in answers:
                tokenized = self.nlp(ans)
                tags = [i.pos_ for i in tokenized]
                phrases = [i for i in tokenized.noun_chunks]
                if (
                    "PROPN" not in tags
                    and "VERB" not in tags
                    and "ADJ" not in tags
                    and phrases != []
                ):
                    return True
        return False


class AdjectivePhraseQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a adjective based phrase
        Returns bool value"""
        if not NumericQuestion().filter(
            context=[], question=[], answers=answers
        ):
            for ans in answers:
                tokenized = self.nlp(ans)
                tags = [i.pos_ for i in tokenized]
                if (
                    "PROPN" not in tags
                    and "VERB" not in tags
                    and "ADJ" in tags
                ):
                    return True
        return False


class VerbPhraseQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_GENERATION, TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(
        self,
        context: str = None,
        question: str = None,
        answers: List[str] = None,
    ) -> bool:
        """Filters out questions whose answer is a verb based phrase
        Returns bool value"""
        if not NumericQuestion().filter(
            context=[], question=[], answers=answers
        ):
            for ans in answers:
                tokenized = self.nlp(ans)
                tags = [i.pos_ for i in tokenized]
                if (
                    "PROPN" not in tags
                    and "VERB" in tags
                    and "ADJ" not in tags
                ):
                    return True
        return False
