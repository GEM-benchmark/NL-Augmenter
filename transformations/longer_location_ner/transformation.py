from typing import List, Tuple
import random
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
A tagging implementation of NER systems.
I am travelling to London. --> I am travelling to South/Central London.
"""


def pick_random_word():
    # pick random "pre" or "post" pertub type with respective word
    pre_word_list = ["East", "West", "South", "North", "Eastern", "Western", "Central"]
    post_word_list = ["City", "Republic"]
    if bool(random.getrandbits(1)):
        pertub_type = "pre"
        selected_word = random.choice(pre_word_list)
    else:
        pertub_type = "post"
        selected_word = random.choice(post_word_list)
    return selected_word, pertub_type


def create_token_and_tag(b_index, i_index, b_tag, i_tag, token_seq, tag_seq, seed):
    random.seed(seed)
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

    def __init__(self, max_outputs=1):
        super().__init__()
        self.max_outputs= max_outputs

    def generate(
        self, token_sequence: List[str], tag_sequence: List[str]
    ) -> List[Tuple[List[str], List[str]]]:
        token_seq = token_sequence.copy()
        tag_seq = tag_sequence.copy()
        perturbed_sentences = []
        tag = "LOCATION" if "B-LOCATION" in tag_seq else "LOC"
        b_tag = "B-" + tag
        i_tag = "I-" + tag
        assert len(token_seq) == len(tag_seq), \
            "Lengths of `token_sequence` and `tag_sequence` should be the same"
        if b_tag in tag_seq:
            b_tag_index = tag_seq.index(b_tag) # find index of b-loc
            i_tag_index = b_tag_index + 1
            for _ in range(self.max_outputs):
                token_seq, tag_seq = create_token_and_tag(b_tag_index, i_tag_index, b_tag, i_tag
                                                                , token_seq, tag_seq, self.seed)
                assert len(token_seq) == len(tag_seq)
                perturbed_sentences.append((token_seq, tag_seq))
                token_seq= token_sequence.copy()
                tag_seq = tag_sequence.copy()
        return perturbed_sentences

# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case
#     tf = LongerLocationNer(max_outputs=1)
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
#     for i, (token_sequence, tag_sequence) in enumerate(zip(src, tgt)):
#         sentences = tf.generate(token_sequence.split(" "), tag_sequence.split(" "))
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"token_sequence": token_sequence, "tag_sequence":tag_sequence},
#             "outputs": []}
#         )
#         for sentence, target in sentences:
#             test_cases[i]["outputs"].append({"token_sequence": " ".join(sentence)
#                                                 , "tag_sequence":" ".join(target)})
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases":test_cases}
#     print(json.dumps(json_file))