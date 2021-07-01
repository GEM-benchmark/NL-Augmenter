from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from typing import Any, Callable, Dict, List, Optional, Union
from transformations.text_typo_transformation.augmenter import typo as a
import random


def simulate_typos(
    texts: Union[str, List[str]],
    aug_char_p: float = 0.3,
    aug_word_p: float = 0.3,
    min_char: int = 2,
    aug_char_min: int = 1,
    aug_char_max: int = 1,
    aug_word_min: int = 1,
    aug_word_max: int = 1000,
    n: int = 1,
    misspelling_dict_path: str = "transformations/text_typo_transformation/misspelling.json",
    priority_words: Optional[List[str]] = None,
) -> List[str]:
    """
    Simulates typos in each text using misspellings, keyboard distance, and swapping

    @param texts: a string or a list of text documents to be augmented

    @param aug_char_p: probability of letters to be replaced in each word;
        This is only applicable for keyboard distance and swapping

    @param aug_word_p: probability of words to be augmented

    @param min_char: minimum # of letters in a word for a valid augmentation;
        This is only applicable for keyboard distance and swapping

    @param aug_char_min: minimum # of letters to be replaced/swapped in each word;
        This is only applicable for keyboard distance and swapping

    @param aug_char_max: maximum # of letters to be replaced/swapped in each word;
        This is only applicable for keyboard distance and swapping

    @param aug_word_min: minimum # of words to be augmented

    @param aug_word_max: maximum # of words to be augmented

    @param n: number of augmentations to be performed for each text

    @param misspelling_dict_path: iopath uri where the misspelling dictionary is stored

    @param priority_words: list of target words that the augmenter should
        prioritize to augment first

    @returns: the list of augmented text documents
    """
    typo_aug = a.TypoAugmenter(
        min_char,
        aug_char_min,
        aug_char_max,
        aug_char_p,
        aug_word_min,
        aug_word_max,
        aug_word_p,
        misspelling_dict_path,
        priority_words,
    )
    aug_texts = typo_aug.augment(texts, n)
    return aug_texts


class TextTypoTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        self.max_output = max_output
        random.seed(self.seed)

    def generate(self, sentence: str):
        return [simulate_typos(sentence)]


"""
# # Sample code to demonstrate usage. Can also assist in adding test cases.
# # You don't need to keep this code in your transformation.
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = TextTypoTransformation(max_output=3)
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
"""
