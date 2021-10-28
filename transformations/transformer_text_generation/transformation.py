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

""" The following transformation generates next word(s) in a sequence based on the prefix of the 
original text, with an option to preserve the label of the original sample.  
"""
class TransformerTextGeneration(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    heavy = True
    keywords = ["text-generation", "transformer"]

    def __init__(
        self,
        eos: str = "</s>",
        no_cuda: bool = False,
        dataset: str = "sst2",
        labeled: bool = True,
        seed: int = 42
    ):
        '''
        Initialization.

                Parameters:
                        eos (str): end of sentence string used by the model.
                        no_cuda (bool): if True, it disables all cuda stuff.
                        dataset (str): dataset with labeled data used to fine-tune model
                        labeled (bool): if True, preserve the label of the original sample
                        during augmentation.
                        seed (int): random seed.
        '''

        super().__init__()
        set_seed(seed, no_cuda)

        model_text_generation: str = "gpt2-xl"
        model_sentiment_classification = None

        if labeled:
            if dataset == "imdb":
                model_text_generation: str = "jmamou/gpt2-medium-IMDB"
                model_sentiment_classification = "textattack/roberta-base-imdb"
            elif dataset == "sst2":
                model_text_generation: str = "jmamou/gpt2-medium-SST-2"
                model_sentiment_classification = (
                    "textattack/roberta-base-SST-2"
                )

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
        max_length_factor:int = 3,
        max_prefix_length:int = 400,
        model_max_length:int = 512,
        temperature: float = 1.0,
        repetition_penalty: float = 1.2,
        k: int = 0,
        p: float = 0.9,
    ):
        '''
        generates next word(s) in a sequence based on the prefix of the original text.

                Parameters:
                        sequence (str): the original text.
                        num_return_sequences (int): the number of sequences to generate.
                        prefix_ratio (float): the ratio of words to define as prefix sequence.
                        max_length_factor (int): factor to define the maximal length (number of
                        tokens) of the generated sequence as a multiplication of the length of the
                        orignal text sequence.
                        max_prefix_length (int): the maximal length of the prefix of the
                        original text.
                        model_max_length (int): the maximal sequence length of the model.
                        temperature (float): the value used to module the next token probabilities.
                        repetition_penalty (float): the parameter for repetition penalty. 1.0
                        means no penalty.
                        k (int): the number of highest probability vocabulary tokens to keep for top-k-filtering.
                        p (float): if set to float < 1, only the most probable tokens with
                        probabilities that add up to p or higher are kept for generation.

                Returns:
                        augmented_texts (list of str): list of augmented sequences
        '''

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
            text = seq["generated_text"]
            if self.text_classifier is not None:
                text = text.split("\t")[1]
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
