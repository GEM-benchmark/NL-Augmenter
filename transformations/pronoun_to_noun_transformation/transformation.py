from abc import ABC

import torch

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformers import (
    AutoModelForMaskedLM,
    AutoTokenizer,
    AutoModelForTokenClassification,
)
from transformers.pipelines.token_classification import (
    TokenClassificationPipeline,
    AggregationStrategy,
)
from transformers import pipeline
import re

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class PronounToNounTransformation(SentenceOperation, ABC):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.QUESTION_ANSWERING,
        TaskType.SENTIMENT_ANALYSIS,
    ]
    languages = ["en"]

    def __init__(
        self,
        ner_model="dslim/bert-base-NER",
        ner_tokenizer="dslim/bert-base-NER",
        masking_model="distilroberta-base",
        match_entities=("PER"),
    ):
        super().__init__()
        self.ner = TokenClassificationPipeline(
            aggregation_strategy=AggregationStrategy.SIMPLE,
            model=AutoModelForTokenClassification.from_pretrained(ner_model),
            tokenizer=AutoTokenizer.from_pretrained(ner_tokenizer, use_fast=True),
        )
        self.mask = pipeline(
            "fill-mask",
            model=AutoModelForMaskedLM.from_pretrained(masking_model),
            tokenizer=AutoTokenizer.from_pretrained(masking_model, use_fast=True),
        )
        self.match_entities = match_entities

    def generate(self, sentence: str):
        entities = [
            entity
            for entity in self.ner(sentence)
            if entity["entity_group"] in self.match_entities
        ]
        masked_sentence = sentence
        for entity in entities:
            start = entity["start"]
            end = entity["end"]
            masked_sentence = (
                masked_sentence[0:start] + "<mask>" + masked_sentence[end:]
            )
            masked_sentence = self.mask(masked_sentence)[0]["sequence"]
        return masked_sentence
