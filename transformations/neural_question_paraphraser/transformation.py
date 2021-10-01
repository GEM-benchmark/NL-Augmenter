import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import numpy as np
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class NeuralParaphaserPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = ["transformer-based", "high-coverage", "high-generations"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        self.max_output = max_output
        self.model = T5ForConditionalGeneration.from_pretrained(
            "ramsrigouthamg/t5_paraphraser"
        )
        self.tokenizer = T5Tokenizer.from_pretrained("ramsrigouthamg/t5_paraphraser")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

    def get_response(self, input_text):
        if not self.is_question(input_text):
            return input_text
        else:
            encoding = self.tokenizer.encode_plus(
                input_text, pad_to_max_length=True, return_tensors="pt"
            )
            input_ids, attention_masks = encoding["input_ids"].to(self.device), encoding[
                "attention_mask"
            ].to(self.device)

            # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3

            beam_outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_masks,
                do_sample=True,
                max_length=256,
                top_k=self.max_output + 1,  # ensure we are different
                top_p=0.9,
                early_stopping=True,
                num_return_sequences=self.max_output,
            )
            final_outputs = []
            for beam_output in beam_outputs:
                sent = self.tokenizer.decode(
                    beam_output, skip_special_tokens=True, clean_up_tokenization_spaces=True
                )
                if sent.lower() != input_text.lower() and sent not in final_outputs:
                    final_outputs.append(sent)
            return final_outputs

    def generate(self, sentence: str):
        perturbed_texts = self.get_response(sentence)
        return perturbed_texts

    def is_question(self, sentence: str):
        "Simple heuristic to know if we are processing a question"
        return "?" in sentence
