import re

from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceAndTargetOperation
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class Concat(SentenceAndTargetOperation):
    """
    This method concatenates two random sentences to create data 
    that has context diversity, length diversity, and 
    (to a lesser extent) position shifting.
    Note that in Nguyen et al., 2021, concatenating consecutive
    and random sentences yielded the same performance gains. Here,
    we concatenate the last sentence the generator saw. Depending on
    how the generate function is called, this could be sequential or
    random - but it does not matter to performance gains.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "ar", "ca", "cs", "da", "de", 
        "en", "eo", "es", "fi", "fr", 
        "ga", "gl", "gu", "he", "hi", 
        "id", "is", "it", "kn", "la", 
        "lt", "mr", "ms", "no", "pa", 
        "pl", "pt", "ro", "ru", "sd", 
        "sk", "sl", "sv", "sw", "ta", 
        "te", "uk", "ur", "vi" 
    ]
    tgt_languages = [
        "ar", "ca", "cs", "da", "de", 
        "en", "eo", "es", "fi", "fr", 
        "ga", "gl", "gu", "he", "hi", 
        "id", "is", "it", "kn", "la", 
        "lt", "mr", "ms", "no", "pa", 
        "pl", "pt", "ro", "ru", "sd", 
        "sk", "sl", "sv", "sw", "ta", 
        "te", "uk", "ur", "vi" 
    ]

    def __init__(
        self, seed=0, max_outputs=1, last_source="", last_target=""
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.last_source=last_source
        self.last_target=last_target

    def generate(self, sentence: str, target: str):
        perturbed_source = sentence + " " + self.last_source
        perturbed_target = target + " " + self.last_target
        self.last_source = sentence
        self.last_target = target


        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}\nLabel: {perturbed_target}"
            )
        return [(perturbed_source, perturbed_target)]

class Concat(SentenceOperation):
    """
    This method concatenates two random sentences to create data 
    that has context diversity, length diversity, and 
    (to a lesser extent) position shifting.
    Note that in Nguyen et al., 2021, concatenating consecutive
    and random sentences yielded the same performance gains. Here,
    we concatenate the last sentence the generator saw. Depending on
    how the generate function is called, this could be sequential or
    random - but it does not matter to performance gains.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "ar", "ca", "cs", "da", "de", 
        "en", "eo", "es", "fi", "fr", 
        "ga", "gl", "gu", "he", "hi", 
        "id", "is", "it", "kn", "la", 
        "lt", "mr", "ms", "no", "pa", 
        "pl", "pt", "ro", "ru", "sd", 
        "sk", "sl", "sv", "sw", "ta", 
        "te", "uk", "ur", "vi" 
    ]

    def __init__(
        self, seed=0, max_outputs=1, last_source=""
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.last_source=last_source

    def generate(self, sentence: str, target: str):
        perturbed_source = sentence + " " + self.last_source
        self.last_source = sentence


        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}"
            )
        return perturbed_source


"""
# Sample code to demonstrate adding test cases.

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = Concat()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    src = ["Andrew finally returned the French book to Chris that I bought last week",
           "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate"
           " to indicate the relation between two or more arguments."]
    tgt = ["Andrew did not return the French book to Chris that was bought earlier",
           "Gapped sentences such as Paul likes coffee and Mary tea, lack an overt predicate!", ]
    for idx, (sentence, target) in enumerate(zip(src, tgt)):
        perturbeds = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": []}
        )
        for sentence, target in perturbeds:
            test_cases[idx]["outputs"].append({"sentence": sentence, "target": target})
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
