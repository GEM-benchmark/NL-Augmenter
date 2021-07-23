import logging
import random
from typing import Callable, Dict, List, Union

import numpy as np
import torch
from sacrebleu import sentence_bleu
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(name="protaugment_diverse_paraphrase")

"""
Protaugment's diverse paraphrase generation, from https://github.com/tdopierre/ProtAugment
"""


def set_seeds(seed: int) -> None:
    """
    set random seeds
    :param seed: int
    :return: None
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def bleu_score(src: str, dst: str):
    return sentence_bleu(dst, [src]).score


def filter_generated_texts_with_distance_metric(
    src: str,
    texts: List[List[str]],
    distance_metric_fn: Callable[[str, str], float],
    lower_is_better: bool = True,
):
    """
    This function aims at selecting one representative in each group of texts (`texts`). Such texts are compared to a source sentence (
    Args:
        src: an original piece of text
        texts: a list of lists of texts
        distance_metric_fn: function to use to compare two texts
        lower_is_better: boolean indicating if a lower value of `distance_metric_fn` is better

    Returns:

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
        super().__init__()
        self.drop_chance = drop_chance

    def bad_words_ids(
        self, input_ids: torch.Tensor, special_ids: List[str] = None
    ) -> List[List[str]]:
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
        super().__init__()

    def bad_words_ids(
        self, input_ids: torch.Tensor, special_ids: List[str] = None
    ) -> List[List[str]]:
        bad_words_ids = list()
        for row in input_ids.tolist():
            if special_ids:
                row = [item for item in row if item not in special_ids]
            for i in range(0, len(row) - 1):
                bad_words_ids.append(row[i: i + 2])
        return bad_words_ids


class ProtaugmentDiverseParaphrase(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = ["en"]

    def __init__(
        self,
        seed: int = 0,
        num_beams: int = 20,
        beam_group_size: int = 4,
        diversity_penalty: float = 0.5,
        device: Union[torch.device, str] = "auto",
        forbid_strategy: Union[ForbidStrategy, str, None] = None,
    ):
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
        batch = self.tokenizer.prepare_seq2seq_batch(
            src_texts=[sentence], return_tensors="pt", max_length=512
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
        return batch

    def generate(self, sentence: str):
        batch = self.prepare_batch(sentence=sentence)
        max_length = batch["input_ids"].shape[1]
        with torch.no_grad():
            preds = self.model.generate(
                **batch,
                max_length=max_length,
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
                tgt_texts[i: i + self.beam_group_size]
                for i in range(0, len(tgt_texts), self.beam_group_size)
            ],
            src=sentence,
            distance_metric_fn=bleu_score,
            lower_is_better=True,
        )

        return filtered


# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    test_cases = []

    for arg_dict in (
        {"forbid_strategy": "bigram"},
        {"forbid_strategy": "unigram"},
    ):
        tf = ProtaugmentDiverseParaphrase(**arg_dict)

        for sentence in [
            "Andrew finally returned the French book to Chris that I bought last week",
            "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
            "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
            "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
            "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
        ]:
            test_cases.append(
                {
                    "class": tf.name(),
                    "args": arg_dict,
                    "inputs": {"sentence": sentence},
                    "outputs": [
                        {"sentence": o} for o in tf.generate(sentence)
                    ],
                }
            )
    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    with open(
        "transformations/protaugment_diverse_paraphrase/test.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(json_file, file, indent=2, ensure_ascii=False)
    print(json.dumps(json_file, indent=2, ensure_ascii=False))
