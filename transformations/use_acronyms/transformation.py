import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Use Acronyms.
    Change groups of words for their equivalent acronym.
    The acronyms were scraped from Wikipedia's List of Acronyms and naively filtered.
"""


def transformation(sentence, lowercase, acronyms):
    new_sentence = sentence
    lower_sentece = sentence.lower()
    for key in acronyms.keys():
        lower_key = key.lower()
        if key in new_sentence:
            new_sentence = new_sentence.replace(key, acronyms[key])
        elif lowercase and (lower_key in lower_sentece):
            key_index = lower_sentece.index(lower_key)
            key_end = key_index + len(key)
            new_sentence = (
                new_sentence[:key_index]
                + acronyms[key]
                + new_sentence[key_end:]
            )

    return new_sentence


class UseAcronyms(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "high-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        lowercase=False,
        acronyms_file_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "acronyms.tsv"
        ),
        sep="\t",
        encoding="utf-8",
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.lowercase = lowercase
        # Load acronyms from file
        temp_acronyms = {}
        with open(acronyms_file_path, "r", encoding=encoding) as file:
            for line in file:
                key, value = line.strip().split(sep)
                temp_acronyms[key] = value
        self.acronyms = temp_acronyms

    def generate(self, sentence: str):
        return [transformation(sentence, self.lowercase, self.acronyms)]


# """
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = UseAcronyms()
    test_cases = []
    for sentence in [
        "I studied at New York University and Massachusetts Institute of Technology.",
        "They changed my connection flight from Newark Liberty International Airport to Los Angeles International Airport.",
        "My brother works at the Center for Science in the Public Interest.",
        "Electro-Optical Tactical Sensor are a fundamental part of the system.",
        "A strong ElectroMagnetic Pulse will damage nearby electronic devices.",
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
# """
