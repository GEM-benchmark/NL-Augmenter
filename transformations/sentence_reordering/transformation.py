import random

# for sent tokenizer
import spacy

# coref resolution from allennlp
# ref: https://demo.allennlp.org/coreference-resolution
from allennlp.predictors.predictor import Predictor

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Shuffle sentence order
"""


class SentenceReordering(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    heavy = True

    def __init__(self, enable_coref=True, seed=42, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.enable_coref = enable_coref
        if enable_coref:
            self.coref_model = Predictor.from_path(
                "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
            )

    def generate(self, sentence: str):
        perturbed = [self.sentence_reordering(text=sentence)]
        return perturbed

    def sentence_reordering(self, text):
        random.seed(self.seed)
        # resolve coref
        if self.enable_coref:
            try:
                text = self.coref_model.coref_resolved(document=text)
            except Exception:
                pass

        # tokenize and shuffle
        text_split = [i.text for i in self.nlp(text).sents]
        random.shuffle(text_split)
        return " ".join(text_split)
