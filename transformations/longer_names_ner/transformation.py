import itertools
import random
from typing import List, Tuple

from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
A tagging implementation for NER systems.
John Smith cooked a curry in the evening. --> John D. Smith cooked a curry in the evening.
"""


class LongerNamesNer(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    languages = "All"
    no_of_repeats = 2  # values should not be larger than 3-4

    def __init__(self, seed=0, no_of_repeats=2, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.no_of_repeats = no_of_repeats

    def generate(
        self, token_sequence: List[str], tag_sequence: List[str]
    ) -> List[Tuple[List[str], List[str]]]:
        random.seed(self.seed)
        token_seq = token_sequence.copy()
        tag_seq = tag_sequence.copy()
        perturbed_sentences = []
        # TODO: Currently perturb only the first name in the sentence. Needs to handle for other names.
        tag = "PERSON" if "B-PERSON" in tag_seq else "PER"
        b_tag = "B-" + tag
        i_tag = "I-" + tag
        assert len(token_seq) == len(
            tag_seq
        ), "Lengths of `token_seq` and `tag_seq` should be the same"
        if b_tag in tag_seq:
            begin = tag_seq.index(b_tag)
            next = begin + 1
            for _ in itertools.repeat(None, self.max_outputs):
                if next < len(tag_seq) and i_tag == tag_seq[next]:
                    for _ in range(self.no_of_repeats):
                        random_upper_letter = chr(
                            random.randint(ord("A"), ord("Z"))
                        )
                        token_seq.insert(next, random_upper_letter)
                        tag_seq.insert(next, i_tag)
                    perturbed_sentences.append((token_seq, tag_seq))
                    token_seq = token_sequence.copy()
                    tag_seq = tag_sequence.copy()
        return perturbed_sentences


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = LongerNamesNer(max_outputs=3)
    test_cases = []
    src = ["Manmohan Singh served as the PM of India .",
           "Neil Alden Armstrong was an American astronaut",
           "Katheryn Elizabeth Hudson is an American singer",
           "The owner of the mall is Anthony Gonsalves.",
           "Roger Michael Humphrey Binny ( born 19 July 1955 ) is an Indian former cricketer ."]
    tgt = ["B-PER I-PER O O O O O B-COUNTRY O",
           "B-PER I-PER I-PER O O B-COUNTRY O",
           "B-PER I-PER I-PER O O B-COUNTRY O",
           "O O O O O O B-PER I-PER",
           "B-PER I-PER I-PER I-PER O O B-DATE I-DATE I-DATE O O O O O O O"
           ]
    for idx, (token_sequence, tag_sequence) in enumerate(zip(src, tgt)):
        sentences = tf.generate(token_sequence.split(" "), tag_sequence.split(" "))
        test_cases.append({
            "class": tf.name(),
            "inputs": {"token_sequence": token_sequence, "tag_sequence": tag_sequence},
            "outputs": []}
        )
        for sentence, target in sentences:
            test_cases[idx]["outputs"].append({"token_sequence": " ".join(sentence), "tag_sequence": " ".join(target)})

    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
