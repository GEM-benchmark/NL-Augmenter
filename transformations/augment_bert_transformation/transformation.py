import itertools
import random
from transformers import *

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class AugmentBERTTransformation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        random.seed(seed)
        hf_model_id = "bert-base-cased"
        self.max_output = max_output
        self.tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
        self.model = AutoModelWithLMHead.from_pretrained(hf_model_id)
        self.pipeline = pipeline(
            "fill-mask",
            model=self.model,
            tokenizer=self.tokenizer,
            framework="pt",
            top_k=2,
        )  # top_k=2 to ensure the augmented sentence is different from the input

    def generate(self, sentence: str):
        perturbed_texts = [
            self.bert_augment(text=sentence) for _ in range(self.max_output)
        ]  # draw a new work each time
        return perturbed_texts

    def bert_augment(self, text):
        """
        :param text: one string text
        :return: on augmented sentence
        """
        assert isinstance(text, str)
        input_ids = self.tokenizer(text, add_special_tokens=False)["input_ids"]
        id_to_mask = random.randint(
            1, len(input_ids) - 2
        )  # select index of subwork to mask
        input_ids[
            id_to_mask
        ] = self.tokenizer.mask_token_id  # replace subwork by mask_token_id
        masked_sentence = self.tokenizer.decode(
            input_ids,
        )
        proposed_sentences = self.pipeline(masked_sentence)
        output_sentences = [s["sequence"] for s in proposed_sentences]
        return (
            output_sentences[0] if output_sentences[0] != text else output_sentences[1]
        )


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
"""
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = AugmentBERTTransformation(max_output=1)
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
