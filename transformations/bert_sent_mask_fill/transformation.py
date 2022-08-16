from transformers import pipeline
from string import punctuation
import spacy
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from typing import List
import torch
import random

"""
The following transformation augments text using mask filling to replace keywords with other words. 
For that, the words that can be masked are found using spacy to extract keywords from a sentence. 
Once the keywords are found, they are replaced with a mask and fed to the BERT model to predict a word in place of the masked word.
"""


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class BertSentenceMaskFilling(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]

    heavy = True
    languages = ["en"]
    """
    Could support other languages if there is a pretrained BERT mask fill model and
    SpaCy model available for the same.
    """

    def __init__(
        self,
        mask_model_name="bert-base-uncased",
        spacy_model_name="en_core_web_sm",
        n_mask_predictions=3,
        seed=0,
    ):
        super().__init__(seed=seed)

        self.n_mask_predictions = n_mask_predictions

        if self.verbose:
            print("Loading BERT Mask Fill Model..\n")

        self.mask_augmenter = pipeline("fill-mask", model=mask_model_name)

        if self.verbose:
            print("Loading SpaCy Model..\n")

        self.nlp = spacy.load(spacy_model_name)
        set_seed(seed)

        if self.verbose:
            print("Completed loading BERT Mask Fill and SpaCy Models..\n")

    def extract_keywords(self, sentence):
        result = []
        pos_tag = ["PROPN", "NOUN", "ADJ", "NUM"]

        doc = self.nlp(sentence)

        for token in doc:
            if (
                token.text in self.nlp.Defaults.stop_words or token.text in punctuation
            ) and token.pos_ not in consider_tags:
                continue
            if token.pos_ in pos_tag:
                result.append(token.text)
        return list(set(result))

    def generate(self, sentence: str) -> List[str]:
        keywords = self.extract_keywords(sentence)
        augmented_sents = []
        for keyword in keywords:
            masked_sent = sentence.replace(
                keyword, self.mask_augmenter.tokenizer.mask_token, 1
            )
            augmented_sents.extend(
                [
                    generated_sent["sequence"].capitalize()
                    for generated_sent in self.mask_augmenter(
                        masked_sent, top_k=self.n_mask_predictions
                    )
                    if generated_sent["sequence"].lower() != sentence.lower()
                ]
            )
        return augmented_sents
