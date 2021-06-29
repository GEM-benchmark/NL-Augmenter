import random
from collections import namedtuple
from typing import Any, List, Literal, Set, Tuple, get_args

import spacy
import torch
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformers import pipeline

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


class TransformerReplace(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "en"
    ]  # could support other types through different spacy/transformer model combinations
    heavy = True

    def __init__(
        self,
        replace_probability=0.2,
        spacy_model="en_core_web_sm",
        transformer_model="distilroberta-base",
        top_k=5,
        device=-1,
        pos_tokens: Set[Literal[POS_TYPES]] = set(get_args(POS_TYPES)),
        sample_top_k=False,
    ):
        super().__init__()
        self.replace_probability = replace_probability
        self.nlp = spacy.load(spacy_model)
        self.fill_pipeline = pipeline(
            "fill-mask", model=transformer_model, top_k=top_k, device=device
        )
        self.pos_tokens = pos_tokens
        self.sample_top_k = sample_top_k
        random.seed(self.seed)

    def _replace_tokens(self) -> bool:
        return random.random() < self.replace_probability

    def get_masked_sentences_from_sentence(
        self, doc: spacy.tokens.Doc
    ) -> Tuple[List[str], List[OriginalWord]]:
        masked_texts = []
        original_words = []
        for token in doc:
            if token.pos_ in self.pos_tokens and self._replace_tokens():
                masked_texts.append(
                    (
                        doc[: token.i].text
                        + " "
                        + self.fill_pipeline.tokenizer.mask_token
                        + " "
                        + doc[token.i + 1 :].text
                    ).strip()
                )
                original_words.append(OriginalWord(token.i, token.text))
        return (masked_texts, original_words)

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
        for i, (preds, original_word) in enumerate(zip(predictions, original_words)):
            predicted_scores = []
            predicted_words = []
            for p in preds:
                if p["token_str"].strip() != original_word.text:
                    predicted_scores.append(p["score"])
                    predicted_words.append(p["token_str"])

            # predict from scores
            if self.sample_top_k:
                x = torch.nn.functional.softmax(torch.tensor(predicted_scores), dim=0)
                cat_dist = torch.distributions.categorical.Categorical(x)
                selected_predicted_index = cat_dist.sample().item()
            else:
                selected_predicted_index = torch.tensor(predicted_scores).argmax()

            new_text += predicted_words[selected_predicted_index]

            # if there is another word to replace - append text in-between
            if i + 1 < len(original_words):
                new_text += (
                    " "
                    + doc[
                        original_words[i].index + 1 : original_words[i + 1].index
                    ].text
                )
            # else if last word then complete sentence
            elif i + 1 == len(original_words):
                new_text += " " + doc[original_words[i].index + 1 :].text
        return new_text

    def generate(self, sentence: str) -> List[str]:
        doc = self.nlp(sentence)
        masked_texts, original_words = self.get_masked_sentences_from_sentence(doc)
        if len(masked_texts) > 0:
            predictions = self.fill_pipeline(masked_texts)
            new_sentence = self.generate_from_predictions(
                doc, predictions, original_words
            )
            return [new_sentence]
        else:
            return [sentence]


# """
# # Sample code to demonstrate usage. Can also assist in adding test cases.
# # You don't need to keep this code in your transformation.
# if __name__ == '__main__':
#     import jsontransformation.py
#     from TestRunner import convert_to_snake_case

#     tf = ButterFingersPerturbation(max_output=3)
#     sentence = "Andrew finally returned the French book to Chris that I bought last week"
#     test_cases = []
#     for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
#                      "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
#                      "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
#                      "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
#                      "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
#         )
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json.dumps(json_file))
# """
