import re

import nltk
import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.style_paraphraser.paraphraser_helpers.style_paraphraser import (
    GPT2ParentModule,
    Instance,
    _beam_search,
    _sample_sequence,
)

"""
    Note: This codebase is based upon, adapted and refactored from code
    from this repository:
    https://github.com/martiansideofthemoon/style-transfer-paraphrase

"""

MODELS_SUPPORTED = {
    "Bible": "filco306/gpt2-bible-paraphraser",
    "Basic": "filco306/gpt2-base-style-paraphraser",
    "Shakespeare": "filco306/gpt2-shakespeare-paraphraser",
    "Tweets": "filco306/gpt2-tweet-paraphraser",
    "Switchboard": "filco306/gpt2-switchboard-paraphraser",
    "Romantic poetry": "filco306/gpt2-romantic-poetry-paraphraser",
}

MAX_PARAPHRASE_LENGTH = 100

BASE_CONFIG = {
    "max_total_length": MAX_PARAPHRASE_LENGTH,
    "max_prefix_length": int(MAX_PARAPHRASE_LENGTH / 2),
    "max_suffix_length": int(MAX_PARAPHRASE_LENGTH / 2),
}


class StyleTransferParaphraser(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    """
        Style transfer paraphraser, using a GPT2-model of choice.

        Args:
            style : str
                The style to use. Options include Bible, Shakespeare, Basic, Romantic Poetry and Tweets.
            device : device to use for computations.
                Default: None, and it will then resort to CUDA if available, else CPU.
            upper_length :
                The maximum length.
                Options: "eos" or "same_N" (e.g., "same_5"), where N will be the max_length.
            beam_size : size of the beam during beam search (if top_p == 0.0)
                Default: 1
            top_p : float
                top_p sampling, between 0.0 and 1.0
                Default: 0.0 (meaning using a greedy approach)
            temperate : float
                Sampling temperate
                Default: 0.0
    """

    def __init__(
        self,
        style: str = "Basic",
        device=None,
        upper_length="same_5",
        beam_size: int = 1,
        top_p: int = 0.0,
        temperature: float = 0.0,
    ):
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        self.style = style

        assert (
            style in MODELS_SUPPORTED.keys()
        ), f"Style not supported. The following styles are supported: {', '.join(list(MODELS_SUPPORTED.keys()))}"
        model_path = MODELS_SUPPORTED[style]
        self.args = {}
        self.device = device
        if self.device is None:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
        self.args["upper_length"] = upper_length
        self.args["stop_token"] = "eos" if upper_length == "eos" else None
        self.args["beam_size"] = beam_size
        self.args["temperature"] = temperature
        self.args["top_p"] = top_p
        self.args["top_k"] = 1
        self.args["device"] = self.device
        self.config = BASE_CONFIG

        self.config["global_dense_length"] = 0
        model = GPT2LMHeadModel.from_pretrained(model_path)
        model.to(self.device)
        self.gpt2_model = GPT2ParentModule(gpt2=model, device=device)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)

    def modify_p(self, top_p):
        """Set top_p to another value"""
        self.args["top_p"] = top_p

    def generate(self, sentence, top_p=None, n_samples: int = 1):
        """
        Generate paraphrases for a batch of outputs - or for the same but with a top_p != 0.0
        sentence : str
            Sentence to paraphrase.
        top_p : float
            top_p sampling, between 0.0 and 1.0
            Default None, resorting to the model's top_p value
        n_samples : int
            Number of samples to generate for a sentence.
            Note: These will be the exact same if you use a greedy sampling (top_p=0.0), so if n_samples > 2, makes sure top_p != 0.0.
        """
        sent_text = nltk.sent_tokenize(sentence)

        contexts = [sent_text] * n_samples

        to_ret = []
        for context_ in contexts:
            instances = []
            for context in context_:
                context_ids = self.tokenizer.convert_tokens_to_ids(
                    self.tokenizer.tokenize(context)
                )

                instance = Instance(
                    self.args,
                    self.config,
                    {"sent1_tokens": context_ids, "sent2_tokens": context_ids},
                )
                instance.preprocess(self.tokenizer)
                global_dense_vectors = np.zeros((1, 768), dtype=np.float32)
                instance.gdv = global_dense_vectors
                instances.append(instance)

            gpt2_sentences = torch.tensor(
                [inst.sentence for inst in instances]
            ).to(self.device)
            segments = torch.tensor([inst.segment for inst in instances]).to(
                self.device
            )
            init_context_size = instances[0].init_context_size
            eos_token_id = self.tokenizer.eos_token_id

            generation_length = (
                None
                if self.args["stop_token"] == "eos"
                else len(gpt2_sentences[0]) - init_context_size
            )

            if self.args["beam_size"] > 1:
                output = _beam_search(
                    model=self.gpt2_model.gpt2,
                    length=generation_length,
                    context=gpt2_sentences[:, 0:init_context_size],
                    segments=segments[:, 0:init_context_size],
                    eos_token_id=eos_token_id,
                    beam_size=self.args["beam_size"],
                    beam_search_scoring=self.args["beam_search_scoring"],
                )
            else:
                output = _sample_sequence(
                    model=self.gpt2_model.gpt2,
                    context=gpt2_sentences[:, 0:init_context_size],
                    segments=segments[:, 0:init_context_size],
                    eos_token_id=eos_token_id,
                    length=generation_length,
                    temperature=self.args["temperature"],
                    top_k=self.args["top_k"],
                    top_p=top_p or self.args["top_p"],
                )

            all_output = []
            for out_num in range(len(output)):
                instance = instances[out_num]
                curr_out = output[
                    out_num, instance.init_context_size :  # noqa: E203
                ].tolist()

                if self.tokenizer.eos_token_id in curr_out:
                    curr_out = curr_out[
                        : curr_out.index(self.tokenizer.eos_token_id)
                    ]

                if self.args["upper_length"].startswith("same"):
                    extra = int(self.args["upper_length"].split("_")[-1])
                    curr_out = curr_out[: len(instance.sent1_tokens) + extra]

                all_output.append(
                    self.tokenizer.decode(
                        curr_out,
                        clean_up_tokenization_spaces=True,
                        skip_special_tokens=True,
                    )
                )
            to_ret.append(re.sub("!?\\??\\.+", ".", ". ".join(all_output)))
        return to_ret[:n_samples]


# Sample code to demonstrate usage of the this perturbation module.
# This can be uncommented to be used to test the module.

"""if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--style", default="Shakespeare", type=str)
    parser.add_argument(
        "--input_sentence",
        default="Hi there! How are you doing today? ",
        type=str,
    )
    parser.add_argument("--top_p_value", default=0.6, type=float)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        print(
            "Please check if a GPU is available or your Pytorch installation is correct."
        )
        sys.exit()

    print("Loading paraphraser...")
    paraphraser = StyleTransferParaphraser(args.style, upper_length="same_5")

    input_sentence = args.input_sentence
    paraphraser.modify_p(top_p=0.0)
    greedy_decoding = paraphraser.generate(input_sentence)
    print("\ngreedy sample:\n{}\n".format(greedy_decoding))

text = "William Shakespeare was an English playwright, poet, and actor, widely regarded as the greatest writer in the English language and the world's greatest dramatist. "
nltk.download("punkt")
sent_text = nltk.sent_tokenize(text)"""
