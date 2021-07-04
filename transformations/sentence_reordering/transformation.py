import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

# for sent tokenizer
import spacy

nlp = spacy.load("en_core_web_sm")

# coref resolution from allennlp
# ref: https://demo.allennlp.org/coreference-resolution
import allennlp_models.tagging
from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
)


"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def sentence_reordering(text, seed, coref_model):
    random.seed(seed)
    # resolve coref
    text = coref_model.coref_resolved(document=text)

    # tokenize and shuffle
    text_split = [i for i in nlp(text).sents]
    random.shuffle(text_split)
    return " ".join(text_split)


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
        self.max_output = max_output
        self.coref_model = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
        )

    def generate(self, sentence: str):
        pertubed = [
            sentence_reordering(
                text=sentence, seed=self.seed, coref_model=self.coref_model
            )
        ]
        return pertubed
