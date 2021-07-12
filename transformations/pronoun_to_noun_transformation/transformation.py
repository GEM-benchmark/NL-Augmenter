import torch

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformers import AutoModelForMaskedLM, AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import re

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class PronounToNounTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.QUESTION_ANSWERING,
        TaskType.SENTIMENT_ANALYSIS,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(
        self,
        ner_model="dslim/bert-base-NER",
        ner_tokenizer="dslim/bert-base-NER",
        masking_model="distilroberta-base",
        match_entities=["B-PER", "I-PER"],
    ):
        self.ner = pipeline(
            "ner",
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
        entities = self.ner(sentence)
        masked_sentence = self.replace_entities_by_mask(
            sentence, entities, self.match_entities
        )
        masked_sentence = self.replace_mask(masked_sentence)

        return self.mask(masked_sentence)

    def replace_entities_by_mask(self, sentence, entities, match_entities):
        masked_sentence = sentence
        for entity in entities:
            tag = entity["entity"]
            if tag in match_entities:
                start = entity["start"]
                end = entity["end"]
                masked_sentence = (
                    masked_sentence[0:start]
                    + "#" * len(masked_sentence[start:end])
                    + masked_sentence[end:]
                )
        return masked_sentence

    def replace_mask(self, masked_sentence):
        return re.sub(r"#\S*#", "<mask>", masked_sentence)
