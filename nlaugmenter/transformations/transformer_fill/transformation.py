import random
from collections import namedtuple
from typing import Any, List, Set, Tuple

import spacy
import torch
from transformers import AutoTokenizer, pipeline
from typing_extensions import Literal, get_args

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

POS_TYPES = Literal[
    "ADJ",
    "ADP",
    "PUNCT",
    "ADV",
    "AUX",
    "SYM",
    "INTJ",
    "CONJ",
    "X",
    "NOUN",
    "DET",
    "PROPN",
    "NUM",
    "VERB",
    "PART",
    "PRON",
    "SCONJ",
]

OriginalWord = namedtuple("OriginalWord", ["index", "text"])


class TransformerFill(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "en"
    ]  # could support other types through different spacy/transformer model combinations
    heavy = True

    def __init__(
        self,
        n: int = 1,
        spacy_model: str = "en_core_web_sm",
        transformer_model: str = "distilroberta-base",
        top_k: int = 5,
        context_text: str = "",
        device: int = -1,
        pos_tokens: Set[Literal[POS_TYPES]] = set(get_args(POS_TYPES)),
        sample_top_k: bool = False,
        seed: int = 0,
    ):
        """
        Args:
            n (int): The number of tokens to change in the sentence.
            spacy_model (str): The spacy model to use to identify tokens by POS tag
            transformer_model (str): The Huggingface transformer model used
            top_k (int): How many candidate words to consider (should be greater > 1 in case word is same as the one being replaced)
            context_text (str): Text to prepend sentence with, to guide model predictions
            device (int): Pass index of GPU if needed
            pos_tokens (Set[Literal[POS_TYPES]]): a set of POS types by which to find potential tokens to replace
            sample_top_k (bool): whether or not to sample from the top_k tokens instead of selecting the best match
        """
        super().__init__(seed=seed)
        self.n = n
        self.nlp = spacy.load(spacy_model, disable=["ner", "lemmatizer"])
        self.fill_pipeline = pipeline(
            "fill-mask", model=transformer_model, top_k=top_k, device=device
        )
        self.pos_tokens = pos_tokens
        self.sample_top_k = sample_top_k

        # context text gets prepended to sentence - can be used to prime transformer predictions
        self.context_text = context_text

        self.tokenizer = AutoTokenizer.from_pretrained(transformer_model)
        self.context_length = len(
            self.tokenizer.encode(
                context_text, truncation=True, add_special_tokens=False
            )
        )

    def truncate(self, text: str) -> str:
        """
        Truncates the passed text or sentence according to the max model length, context length and start/end token
        """
        return self.tokenizer.decode(
            self.tokenizer.encode(
                text,
                truncation=True,
                add_special_tokens=False,
                max_length=self.tokenizer.model_max_length
                - self.context_length
                - 4,
            )
        )

    def get_masked_sentences_from_sentence(
        self, doc: spacy.tokens.Doc
    ) -> Tuple[List[str], List[OriginalWord]]:
        random.seed(self.seed)
        masked_texts = []
        original_words = []
        for token in doc:
            if token.pos_ in self.pos_tokens:
                masked_texts.append(
                    (
                        self.context_text
                        + doc[: token.i].text
                        + " "
                        + self.fill_pipeline.tokenizer.mask_token
                        + " "
                        + doc[token.i + 1 :].text
                    ).strip()
                )
                original_words.append(OriginalWord(token.i, token.text))

        if len(masked_texts) >= self.n:
            # select n words to replace
            selection = random.sample(
                list(zip(masked_texts, original_words)), self.n
            )
            masked_texts, original_words = zip(
                *sorted(selection, key=lambda x: x[1].index)
            )
            return (list(masked_texts), list(original_words))
        return masked_texts, original_words

    def generate_from_predictions(
        self,
        doc: spacy.tokens.Doc,
        predictions: List[Any],
        original_words: List[OriginalWord],
    ) -> str:
        if len(original_words) < 1:
            return doc.text
        elif len(original_words) == 1:
            predictions = [predictions]

        # initial text from beginning of sentence to first word to replace
        new_text = doc[: original_words[0].index].text
        for i, (preds, original_word) in enumerate(
            zip(predictions, original_words)
        ):
            predicted_scores = []
            predicted_words = []
            for p in preds:
                if p["token_str"].strip() != original_word.text:
                    predicted_scores.append(p["score"])
                    predicted_words.append(p["token_str"])

            # predict from scores
            if self.sample_top_k:
                x = torch.nn.functional.softmax(
                    torch.tensor(predicted_scores), dim=0
                )
                cat_dist = torch.distributions.categorical.Categorical(x)
                selected_predicted_index = cat_dist.sample().item()
            else:
                selected_predicted_index = torch.tensor(
                    predicted_scores
                ).argmax()

            new_text += predicted_words[selected_predicted_index]

            # if there is another word to replace - append text in-between
            if i + 1 < len(original_words):
                new_text += (
                    " "
                    + doc[
                        original_words[i].index
                        + 1 : original_words[i + 1].index
                    ].text
                )
            # else if last word then complete sentence
            elif i + 1 == len(original_words):
                new_text += " " + doc[original_words[i].index + 1 :].text
        return new_text.strip()

    def generate(self, sentence: str) -> List[str]:
        truncated_sentence = self.truncate(sentence)
        doc = self.nlp(truncated_sentence, disable=["ner", "lemmatizer"])
        masked_texts, original_words = self.get_masked_sentences_from_sentence(
            doc
        )
        if len(masked_texts) > 0:
            predictions = self.fill_pipeline(masked_texts)
            new_sentence = self.generate_from_predictions(
                doc, predictions, original_words
            )
            return [new_sentence]
        return []
