from nlaugmenter.interfaces.SentenceOperation import SentenceAndTargetOperation
from nlaugmenter.tasks.TaskTypes import TaskType


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

    This is the same transformation as concat_monlingual, but bilingual
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = [
        "ar",
        "ca",
        "cs",
        "da",
        "de",
        "en",
        "eo",
        "es",
        "fi",
        "fr",
        "ga",
        "gl",
        "gu",
        "he",
        "hi",
        "id",
        "is",
        "it",
        "kn",
        "la",
        "lt",
        "mr",
        "ms",
        "no",
        "pa",
        "pl",
        "pt",
        "ro",
        "ru",
        "sd",
        "sk",
        "sl",
        "sv",
        "sw",
        "ta",
        "te",
        "uk",
        "ur",
        "vi",
    ]
    tgt_languages = [
        "ar",
        "ca",
        "cs",
        "da",
        "de",
        "en",
        "eo",
        "es",
        "fi",
        "fr",
        "ga",
        "gl",
        "gu",
        "he",
        "hi",
        "id",
        "is",
        "it",
        "kn",
        "la",
        "lt",
        "mr",
        "ms",
        "no",
        "pa",
        "pl",
        "pt",
        "ro",
        "ru",
        "sd",
        "sk",
        "sl",
        "sv",
        "sw",
        "ta",
        "te",
        "uk",
        "ur",
        "vi",
    ]
    keywords = [
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, max_outputs=1, last_source="", last_target=""):
        super().__init__(seed, max_outputs=max_outputs)
        self.last_source = last_source
        self.last_target = last_target

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
