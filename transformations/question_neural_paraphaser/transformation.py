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


class DialogNeuralParaphaserPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(True)
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


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
"""
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = DialogNeuralParaphaserPerturbation(max_output=1)
    sentence = (
        "Andrew finally returned the French book to Chris that I bought last week"
    )
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
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
    with open("test.json", "w") as f:
        json.dump(json_file, f, indent=4)
