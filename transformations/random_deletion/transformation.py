import numpy as np

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def random_deletion(text, prob=0.1, seed=0):
    np.random.seed(seed)
    text = np.array(text.split())
    N = len(text)
    mask = np.random.binomial(1, 1 - prob, N) == 1
    text_tf = text[mask]
    text_tf = " ".join(text_tf)
    text_tf = (
        text_tf if len(text_tf) > 0 else text[np.random.randint(0, N - 1)]
    )
    return [text_tf]


class RandomDeletion(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, prob=0.25, seed=0):
        super().__init__(seed)
        self.prob = prob

    def generate(self, sentence: str):
        perturbed_texts = random_deletion(
            text=sentence, prob=self.prob, seed=self.seed
        )
        return perturbed_texts


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = RandomDeletion()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    with open("test.json", "w") as f:
        ijson.dump(json_file, f, indent=2)
"""
