import logging
import math

import numpy as np
import torch
from transformers import GPT2LMHeadModel, pipeline

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def set_seed(seed: int, no_cuda: bool):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if not no_cuda:
        torch.cuda.manual_seed_all(seed)


class TransformerTextGeneration(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(
        self,
        eos: str = "</s>",
        no_cuda: bool = False,
        dataset="sst2",
        labeled=True,
        seed=42,
    ):

        set_seed(seed, no_cuda)

        if labeled:
            if dataset == "imdb":
                model_text_generation: str = "jmamou/gpt2-medium-IMDB"
                # model_sentiment_classification = 'aychang/roberta-base-imdb'
                model_sentiment_classification = "textattack/roberta-base-imdb"
            elif dataset == "sst2":
                model_text_generation: str = "jmamou/gpt2-medium-SST-2"
                model_sentiment_classification = (
                    "textattack/roberta-base-SST-2"
                )
        else:
            model_text_generation: str = "gpt2-xl"
            model_sentiment_classification = None

        self.eos = eos
        device = -1 if no_cuda else 0

        # initialize text generation pipeline
        model = GPT2LMHeadModel.from_pretrained(model_text_generation)
        self.text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=model_text_generation,
            device=device,
        )

        # if relevant, initialize the sentiment classification pipeline
        if model_sentiment_classification is not None:
            self.label_name = "label"
            self.text_classifier = pipeline(
                "sentiment-analysis",
                model=model_sentiment_classification,
                tokenizer=model_sentiment_classification,
                device=device,
            )
        else:
            self.text_classifier = None

    def generate(
        self,
        sequence: str,
        num_return_sequences: int = 1,
        prefix_ratio: float = 0.5,
        max_length_factor=3,
        max_prefix_length=400,
        model_max_length=512,
        temperature: float = 1.0,
        repetition_penalty: float = 1.2,
        k: int = 0,
        p: float = 0.9,
    ):

        logger.info("original text: " + sequence)
        augmented_texts = []
        sequence = sequence.split()

        prefix_length = min(
            max_prefix_length, math.ceil(len(sequence) * prefix_ratio)
        )
        if self.text_classifier is None:
            text_inputs = " ".join(sequence[0:prefix_length])
        else:
            label = self.text_classifier(sequence, truncation=True)[0][
                self.label_name
            ]
            label = label.split("_")[1]
            text_inputs = label + "\t" + " ".join(sequence[0:prefix_length])

        max_length = min(model_max_length, len(sequence) * max_length_factor)
        output_sequences = self.text_generator(
            text_inputs=text_inputs,
            temperature=temperature,
            top_k=k,
            top_p=p,
            repetition_penalty=repetition_penalty,
            do_sample=True,
            num_return_sequences=num_return_sequences,
            clean_up_tokenization_spaces=True,
            return_full_text=True,
            max_length=max_length,
            truncation=True,
        )
        for seq in output_sequences:
            text = seq["generated_text"].split("\t")[1]
            text = text[
                : text.find(self.eos)
                if self.eos and text.find(self.eos) > -1
                else None
            ].strip()
            text = text.replace("\n", ".")
            augmented_texts.append(text)
            logger.info("augmented text: " + text)
        return augmented_texts


if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = TransformerTextGeneration()
    test_cases = []
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
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    print(json.dumps(json_file))
