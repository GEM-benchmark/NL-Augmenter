import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class RandomUpperPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1, corrupt_proportion=0.1):
        super().__init__(seed)
        random.seed(seed)
        self.max_output = max_output
        self.corrupt_proportion = corrupt_proportion

    def generate(self, sentence: str):
        perturbed_texts = [self.random_upper(sentence) for _ in range(self.max_output)]
        return perturbed_texts

    def random_upper(self, sentence: str):
        positions = random.sample(
            range(0, len(sentence)), int(len(sentence) * self.corrupt_proportion)
        )
        new_sentence = [
            letter if index not in positions else letter.upper()
            for index, letter in enumerate(sentence)
        ]
        return "".join(new_sentence)


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
"""
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = RandomUpperPerturbation(max_output=1)
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
