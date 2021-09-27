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
    keywords = [
        "lexical",
        "noise",
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
    ]

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

            # In the case of very short inputs, allow for the addition of
            # tokens before/after the first/last token respectively.
            short_input = len(tokens) <= 1
            if short_input:
                tokens = [None] + tokens + [None]

            choices = []
            while not choices:
                for i in range(1, len(tokens)):
                    if random.random() < self.insert_prob:
                        choices.append(i)

            choices = choices[::-1]
            for i in choices:
                tokens.insert(i, random.choice(self.filler_words))

            if short_input:
                tokens = tokens[1:-1]

            perturbed_texts.append(" ".join(tokens))
        return perturbed_texts

"""
# Sample code to demonstrate usage.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = SpeechDisfluencyPerturbation(max_outputs=1)
    test_cases = []
    for sentence in [
        "Andrew finally returned the French book to Chris that I bought last week",
        "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
        "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
        "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
        "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
        "Yes",
        "Of course",
        "",
    ]:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    for filler_words, sentence in [
        (["oof", "agh"], "Where did you learn how to drive again?"),
        (["eek"], "I'm deathly afraid of mice!"),
        (["hmph", "ahem", "wheeze"], "I've had a sore throat all week."),
    ]:
        tf2 = SpeechDisfluencyPerturbation(
            max_outputs=1, filler_words=filler_words
        )
        test_cases.append(
            {
                "class": tf2.name(),
                "args": {"filler_words": filler_words},
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf2.generate(sentence)],
            }
        )

    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    print(json.dumps(json_file, indent=2))
"""
