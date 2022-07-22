import logging
import random
from abc import ABC
from typing import Callable, Dict, List, Union

import numpy as np
import torch
from sacrebleu import sentence_bleu
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(name="protaugment_diverse_paraphrase")
logger.setLevel(logging.INFO)

"""
Protaugment's diverse paraphrase generation, from https://github.com/tdopierre/ProtAugment
"""


def set_seeds(seed: int) -> None:
    """
    Args:
        seed: random seed to set
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def bleu_score(src: str, dst: str) -> float:
    """

    Args:
        src: source sentence (reference)
        dst: target sentence (hypothesis)

    Returns: BLEU score

    """
    return sentence_bleu(dst, [src]).score


def filter_generated_texts_with_distance_metric(
    src: str,
    texts: List[List[str]],
    distance_metric_fn: Callable[[str, str], float],
    lower_is_better: bool = True,
) -> List[str]:
    """
    This function aims at selecting one representative in each group of texts (`texts`). Such texts are compared to a source sentence (src)
    Args:
        src: an original piece of text
        texts: a list of lists of texts
        distance_metric_fn: function to use to compare two texts
        lower_is_better: boolean indicating if a lower value of `distance_metric_fn` is better

    Returns: a list of sentences, one per group. If the shape of `texts` was (M, N), this function would return a list of M sentences.

    """
    scores = [
        [distance_metric_fn(src, text) for text in group] for group in texts
    ]

    if lower_is_better:
        ranking_fn = np.argmin
    else:
        ranking_fn = np.argmax
    return [
        group[ranking_fn(scores_)] for group, scores_ in zip(texts, scores)
    ]


class ForbidStrategy:
    def bad_words_ids(self, input_ids: torch.Tensor) -> List[List[str]]:
        raise NotImplementedError


class UnigramForbidStrategy(ForbidStrategy):
    def __init__(self, drop_chance: float = 0.7):
        """
        Forbidding strategy which randomly forbids tokens based on a fixed probability.
        Args:
            drop_chance: probability of dropping tokens (float between 0 and 1)
        """
        super().__init__()
        self.drop_chance = drop_chance

    def bad_words_ids(
        self, input_ids: torch.Tensor, special_ids: List[int] = None
    ) -> List[List[int]]:
        """
        Args:
            input_ids: Tensor of shape (num_sentences, sentence_length), containing token ids (int).
            special_ids: List[int] containing special ids which will not be forbidden.

        Returns: List[List[int]]
            Returns a list of list of integers, corresponding to sequences of ids.

        """
        bad_words_ids = list()
        for row in input_ids.tolist():
            if special_ids:
                row = [item for item in row if item not in special_ids]

            for item_ix, item in enumerate(row):
                if random.random() < self.drop_chance:
                    bad_words_ids.append(item)

        # Reshape to correct format
        bad_words_ids = [[item] for item in bad_words_ids]
        return bad_words_ids


class BigramForbidStrategy(ForbidStrategy):
    def __init__(self):
        """
        Bi-gram forbidding strategy. All bi-grams will be forbidden.
        """
        super().__init__()

    def bad_words_ids(
        self, input_ids: torch.Tensor, special_ids: List[int] = None
    ) -> List[List[int]]:
        """
        Args:
            input_ids: Tensor of shape (num_sentences, sentence_length), containing token ids (int).
            special_ids: List[int] containing special ids which will not be forbidden.

        Returns: List[List[int]]
            Returns a list of list of integers, corresponding to sequences of ids.:

        """
        bad_words_ids = list()
        for row in input_ids.tolist():
            if special_ids:
                row = [item for item in row if item not in special_ids]
            for i in range(0, len(row) - 1):
                bad_words_ids.append(row[i : i + 2])
        return bad_words_ids


class ProtaugmentDiverseParaphrase(SentenceOperation, ABC):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = ["en"]
    heavy = True
    keywords = [
        # Linguistic change
        "lexical",
        # Type of algorithm
        "model-based",
        "transformer-based",
        "tokenizer-required",
        # Naturalness of the generation
        "unnatural-sounding",
        "unnaturally-written",
        # Potential accuracy & precision of the generation
        "possible-meaning-alteration",
        "high-coverage",
    ]

    def __init__(
        self,
        seed: int = 0,
        num_beams: int = 20,
        beam_group_size: int = 4,
        diversity_penalty: float = 0.5,
        device: Union[torch.device, str] = "auto",
        forbid_strategy: Union[ForbidStrategy, str, None] = None,
    ):
        """
        Args:
            seed: Random seed
            num_beams: Number of total beams
            beam_group_size: Size of group beams. must be a divisor or `num_beams`
            diversity_penalty: Penalty to apply to enforce more diversity. See https://arxiv.org/abs/1610.02424
            device: Device to use
            forbid_strategy: Strategy to use to forbid tokens in the generation step.
        """
        # Random seed
        self.seed = seed
        set_seeds(self.seed)

        # Instancing device
        if type(device) == str:
            if device == "auto":
                device = (
                    torch.device("cuda")
                    if torch.cuda.is_available()
                    else torch.device("cpu")
                )
            else:
                device = torch.device(device)
        self.device = device

        # Instancing parameters
        assert (
            num_beams % beam_group_size == 0
        )  # `num_beams` should be a multiple of `beam_group_size`
        self.num_return_sequences = self.num_beams = num_beams
        self.beam_group_size = beam_group_size
        self.num_beam_groups = self.num_beams // self.beam_group_size
        self.diversity_penalty = diversity_penalty

        if type(forbid_strategy) == str:
            if forbid_strategy == "bigram":
                forbid_strategy = BigramForbidStrategy()
            elif forbid_strategy == "unigram":
                forbid_strategy = UnigramForbidStrategy(drop_chance=0.7)
            else:
                error_msg = f"Forbid stategy defined by string `{forbid_strategy}` not implemented yet."
                logger.error(error_msg)
                raise NotImplementedError(error_msg)

        self.forbid_strategy = forbid_strategy

        self.model_name = "tdopierre/ProtAugment-ParaphraseGenerator"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(
            self.device
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        super().__init__()

    def prepare_batch(
        self, sentence: str
    ) -> Dict[str, Union[torch.Tensor, List[List[str]]]]:
        """

        Args:
            sentence: Sentence to paraphrase.

        Returns: Batch interpretable by the paraphrase generation model

        """
        batch = self.tokenizer.batch_encode_plus(
            batch_text_or_text_pairs=[sentence],
            return_tensors="pt",
            max_length=512,
        )
        batch = {k: v.to(self.device) for k, v in batch.items()}

        # If a forbidding strategy exists, then add those forbidden words to the batch
        if self.forbid_strategy:
            bad_words_ids = self.forbid_strategy.bad_words_ids(
                special_ids=self.tokenizer.all_special_ids,
                input_ids=batch["input_ids"],
            )

            if len(bad_words_ids):
                batch["bad_words_ids"] = bad_words_ids
                bad_words = [
                    [
                        self.tokenizer.decode(word_id)
                        for word_id in bad_ngram_ids
                    ]
                    for bad_ngram_ids in bad_words_ids
                ]
                logger.info(f"Forbidden tokens: {bad_words}")
        return batch

    def generate(self, sentence: str):
        """
        Generates paraphrases for a given sentence
        Args:
            sentence: Sentence to paraphrase

        Returns: A list of paraphrases for the given sentence

        """
        set_seeds(self.seed)
        batch = self.prepare_batch(sentence=sentence)
        with torch.no_grad():
            preds = self.model.generate(
                **batch,
                num_beams=self.num_beams,
                num_beam_groups=self.beam_group_size,
                diversity_penalty=self.diversity_penalty,
                num_return_sequences=self.num_return_sequences,
            )

        tgt_texts = self.tokenizer.batch_decode(
            preds.detach().cpu(), skip_special_tokens=True
        )
        assert (
            len(tgt_texts) == self.num_beams
        ), f"#tgt texts {len(tgt_texts)} does not match num beams {self.num_beams}"

        filtered = filter_generated_texts_with_distance_metric(
            texts=[
                tgt_texts[i : i + self.beam_group_size]
                for i in range(0, len(tgt_texts), self.beam_group_size)
            ],
            src=sentence,
            distance_metric_fn=bleu_score,
            lower_is_better=True,
        )

        return filtered


# Sample code to create test cases.
# if __name__ == "__main__":
#     import json
#
#     from TestRunner import convert_to_snake_case
#
#     test_cases = []
#
#     for arg_dict in (
#             {"forbid_strategy": "bigram"},
#             {"forbid_strategy": "unigram"},
#     ):
#         tf = ProtaugmentDiverseParaphrase(**arg_dict)
#
#         for sentence in [
#             'What should I do if the ATM "stole" my card?',
#             "Please explain your exchange rate policy.",
#             "change my house lights colour to blue",
#             'Add "bohemian rapshody" to my rock playlist',
#             "Which soft drink does Madonna advertise for ?",
#         ]:
#             test_cases.append(
#                 {
#                     "class": tf.name(),
#                     "args": arg_dict,
#                     "inputs": {"sentence": sentence},
#                     "outputs": [
#                         {"sentence": o} for o in tf.generate(sentence)
#                     ],
#                 }
#             )
#     json_file = {
#         "type": convert_to_snake_case(tf.name()),
#         "test_cases": test_cases,
#     }
#     with open(
#             "transformations/protaugment_diverse_paraphrase/test.json",
#             "w",
#             encoding="utf-8",
#     ) as file:
#         json.dump(json_file, file, indent=2, ensure_ascii=False)
#     print(json.dumps(json_file, indent=2, ensure_ascii=False))
