import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

# for sent tokenizer
import spacy

# coref resolution from allennlp
# ref: https://demo.allennlp.org/coreference-resolution
import allennlp_models.tagging
from allennlp.predictors.predictor import Predictor


"""
Shuffle sentence order
"""


class SentenceReordering(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, max_output=1):
        super().__init__(seed)
        self.seed = seed
        self.nlp = spacy.load("en_core_web_sm")
        self.max_output = max_output
        self.coref_model = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
        )

    def generate(self, sentence: str):
        pertubed = [self.sentence_reordering(text=sentence)]
        return pertubed

    def sentence_reordering(self, text):
        random.seed(self.seed)
        # resolve coref
        text = self.coref_model.coref_resolved(document=text)

        # tokenize and shuffle
        text_split = [i.text for i in self.nlp(text).sents]
        random.shuffle(text_split)
        return " ".join(text_split)
