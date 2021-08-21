import random
from typing import List, Optional

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class SpeechDisfluencyPerturbation(SentenceOperation):
    tasks: List[TaskType] = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages: List[str] = ["en"]
    filler_words: List[str] = ["um", "uh", "erm", "ah", "er"]
    insert_prob: float

    def __init__(
        self,
        seed: int = 0,
        max_outputs: int = 1,
        insert_prob: float = 0.2,
        filler_words: Optional[List[str]] = None,
    ) -> None:
        super().__init__(seed, max_outputs=max_outputs)
        self.insert_prob = insert_prob
        if filler_words is not None:
            self.filler_words = filler_words

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)
        perturbed_texts = []

        for _ in range(self.max_outputs):
            tokens = sentence.split()
            choices = []
            while not choices:
                for i in range(1, len(tokens) - 1):
                    if random.random() < self.insert_prob:
                        choices.append(i)

            choices = choices[::-1]
            for i in choices:
                tokens.insert(i, random.choice(self.filler_words))

            perturbed_texts.append(" ".join(tokens))
        return perturbed_texts


# Sample code to demonstrate usage.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = SpeechDisfluencyPerturbation(max_outputs=1)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
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
    print(json.dumps(json_file, indent=2))
