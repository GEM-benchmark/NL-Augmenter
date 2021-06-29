from typing import List
from random import choice, seed, getrandbits
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
A tagging implementation of NER systems.
I am travelling to London. --> I am travelling to South/Central London.
"""


def pick_random_word():
    pre_word_list = ["East", "West", "South", "North", "Eastern", "Western", "Northern", "Central", "New"]
    post_word_list = ["City", "Republic", "Beach"]
    if bool(getrandbits(1)):
        pertub_type = "pre"
        selected_word = choice(pre_word_list)
    else:
        pertub_type = "post"
        selected_word = choice(post_word_list)
    return selected_word, pertub_type


def create_token_and_tag(b_index, i_index, b_tag, i_tag, token_seq, tag_seq):
    word, pertub_type = pick_random_word()
    if pertub_type == "pre":
        token_seq.insert(b_index, word)
        tag_seq.insert(b_index, b_tag)
        tag_seq[i_index] = i_tag
    elif pertub_type == "post":
        token_seq.insert(b_index+1, word)
        tag_seq.insert(b_index+1, i_tag)
    return token_seq, tag_seq


class LongerLocationNer(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    languages = "All"

    def __init__(self):
        super().__init__()

    def generate(
        self, token_sequence: List[str], tag_sequence: List[str]):
        #seed(self.seed)
        token_sequence = token_sequence.copy()
        tag_sequence = tag_sequence.copy()
        tag = "LOCATION" if "B-LOCATION" in tag_sequence else "LOC"
        b_tag = "B-" + tag
        i_tag = "I-" + tag
        assert len(token_sequence) == len(tag_sequence), \
            "Lengths of `token_sequence` and `tag_sequence` should be the same"
        if b_tag in tag_sequence:
            b_tag_index = tag_sequence.index(b_tag)
            i_tag_index = b_tag_index + 1
            token_sequence, tag_sequence = create_token_and_tag(b_tag_index, i_tag_index, b_tag, i_tag
                                                                , token_sequence, tag_sequence)
        assert len(token_sequence) == len(tag_sequence)
        return token_sequence, tag_sequence

# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case
#     tf = LongerLocationNer()
#     test_cases = []
#     src = ["I am travelling to London .",
#            "Edison was born in Ohio .",
#            "Michael Jordan is a professor at Berkeley .",
#            "Google head office is located in California ."]
#     tgt = ["O O O O B-LOC O",
#            "B-PER O O O B-LOC O",
#            "B-PER I-PER O O O O B-LOC O",
#            "B-ORG O O O O O B-LOC O"]
#
#     for token_sequence, tag_sequence in zip(src, tgt):
#         sentence_o, target_o = tf.generate(token_sequence.split(" "), tag_sequence.split(" "))
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"token_sequence": token_sequence, "tag_sequence":tag_sequence},
#             "outputs": {"token_sequence":" ".join(sentence_o), "tag_sequence":" ".join(target_o)}
#         })
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases":test_cases}
#     print(json.dumps(json_file))