from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class ConcatMonolingual(SentenceOperation):
    """
    This method concatenates two random sentences to create data
    that has context diversity, length diversity, and
    (to a lesser extent) position shifting.
    Note that in Nguyen et al., 2021, concatenating consecutive
    and random sentences yielded the same performance gains. Here,
    we concatenate the last sentence the generator saw. Depending on
    how the generate function is called, this could be sequential or
    random - but it does not matter to performance gains.

    Note that this is the same as the concat transformation but is monolingual
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
    keywords = [
        "rule-based",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, max_outputs=1, last_source=""):
        super().__init__(seed, max_outputs=max_outputs)
        self.last_source = last_source

    def generate(self, sentence: str):
        perturbed_source = sentence + " " + self.last_source
        self.last_source = sentence

        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}"
            )
        return [perturbed_source]
