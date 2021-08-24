from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Use Acronyms.
    Change groups of words for their equivalent acronym.
    The acronyms were scraped from Wikipedia's List of Acronyms and naively filtered.
"""


def transformation(sentence, acronyms):
    new_sentence = sentence
    for key in acronyms.keys():
        if key in new_sentence:
            new_sentence = new_sentence.replace(key, acronyms[key])
    return new_sentence


class UseAcronyms(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        acronyms_file="transformations/use_acronyms/acronyms.tsv",
        sep="\t",
        encoding="utf-8",
    ):
        super().__init__(seed, max_outputs=max_outputs)
        acronyms = {}
        with open(acronyms_file, "r", encoding=encoding) as file:
            for line in file:
                key, value = line.strip().split(sep)
                acronyms[key] = value
        self.acronyms = acronyms

    def generate(self, sentence: str):
        return [transformation(sentence, self.acronyms)]


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
