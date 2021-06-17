from typing import List
import random
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

    def __init__(self, no_of_repeats=2):
        super().__init__()
        self.no_of_repeats = no_of_repeats

    def generate(self, token_sequence: List[str], tag_sequence: List[str]):
        random.seed(self.seed)
        token_sequence = token_sequence.copy()
        tag_sequence = tag_sequence.copy()
        tag = "PERSON" if "B-PERSON" in tag_sequence else "PER"
        b_tag = "B-" + tag
        i_tag = "I-" + tag
        assert len(token_sequence) == len(tag_sequence), \
            "Lengths of `token_sequence` and `tag_sequence` should be the same"
        if b_tag in tag_sequence:
            begin = tag_sequence.index(b_tag)
            next = begin + 1
            if next < len(tag_sequence) and i_tag == tag_sequence[next]:
                for _ in range(self.no_of_repeats):
                    random_upper_letter = chr(random.randint(ord("A"), ord("Z")))
                    token_sequence.insert(next, random_upper_letter)
                    tag_sequence.insert(next, i_tag)
        return token_sequence, tag_sequence



"""
# Sample code to demonstrate usage. Can also assist in adding test cases.

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = LongerNamesNer()
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
    for token_sequence, tag_sequence in zip(src, tgt):
        sentence_o, target_o = tf.generate(token_sequence.split(" "), tag_sequence.split(" "))
        test_cases.append({
            "class": tf.name(),
            "inputs": {"token_sequence": token_sequence, "tag_sequence": tag_sequence},
            "outputs": {"token_sequence": " ".join(sentence_o), "tag_sequence": " ".join(target_o)}}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""