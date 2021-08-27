from typing import List, Tuple
import random
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
A tagging implementation of NER systems.
I am travelling to London. --> I am travelling to South/Central London.
"""


def pick_random_word(seed):
    """
    pick random "pre" or "post" perturb type with respective word
    """
    pre_word_list = ["East", "West", "South", "North", "Eastern", "Western", "Central", "Southern",
                     "Northern", "Northeast", "Southwest", "Southeast", "Northwest", "NE", "SW", "SE", "NW",
                     "ESE", "SSE", "SSW", "WSW", "WNW", "NNW", "NNE", "North East", "ENE", "South West",
                     "South East", "North West", "Eastern South East", "Southern South East",
                     "Southern South West", "Western South West", "Western North West", "Northern North West",
                     "Northern North East", "Eastern North East"]
    post_word_list = ["City", "Republic", "University", "Airport", "Palace"]
    random.seed(seed)
    if bool(random.getrandbits(1)):
        perturb_type = "pre"
        selected_word = random.choice(pre_word_list)
    else:
        perturb_type = "post"
        selected_word = random.choice(post_word_list)
    return selected_word, perturb_type


def create_token_and_tag_seq(token_seq, tag_seq, b_tag_index, i_tag_index, b_tag, i_tag, seed):
    """
    Select perturb_type and respected phrase associated with it randomly.
    """
    phrase, perturb_type = pick_random_word(seed)
    if perturb_type == "pre":
        token_seq, tag_seq = add_location_prefix(token_seq, tag_seq, phrase, b_tag_index, b_tag, i_tag)
    if perturb_type == "post":
        token_seq, tag_seq = add_location_postfix(token_seq, tag_seq, phrase, i_tag_index, i_tag)
    return token_seq, tag_seq


def add_location_prefix(token_seq, tag_seq, phrase, b_tag_index, b_tag, i_tag):
    """
        Create token sequence and tag sequence for prefix perturbation
    """
    word_list = phrase.strip().split(" ")
    if len(word_list) == 1:  # if selected phrase contains single word
        token_seq.insert(b_tag_index, phrase)  # put phrase in token_seq at index b_tag_index
        tag_seq[b_tag_index] = i_tag  # replace B-LOC with I-LOC
        tag_seq.insert(b_tag_index, b_tag)  # put B-LOC in tag_seq at index b_tag_index
        return token_seq, tag_seq
    else:  # if selected phrase is multi-word
        for i, word in enumerate(word_list):
            if i == 0:
                tag_seq[b_tag_index] = i_tag  # change B-LOC to I-LOC
                token_seq.insert(b_tag_index, word)
                tag_seq.insert(b_tag_index, b_tag)
            else:
                token_seq.insert(b_tag_index + i, word)
                tag_seq.insert(b_tag_index + i, i_tag)
        return token_seq, tag_seq


def add_location_postfix(token_seq, tag_seq, phrase, i_tag_index, i_tag):
    """
    Create token sequence and tag sequence for postfix perturbation
    """
    word_list = phrase.strip().split(" ")
    if len(word_list) == 1:
        token_seq.insert(i_tag_index + 1, phrase)
        tag_seq.insert(i_tag_index + 1, i_tag)
        return token_seq, tag_seq
    else:
        for i, word in enumerate(word_list):
            i += 1
            token_seq.insert(i_tag_index + i, word)
            tag_seq.insert(i_tag_index + i, i_tag)
        return token_seq, tag_seq


def extract_tag_indexes(tag_seq, b_tag, i_tag):
    """
    Returns index of B-LOC and I-LOC, I-LOC = -1 if no I-LOC exist
    """
    i_tag_index = -1  # default value
    b_tag_index = tag_seq.index(b_tag)
    if b_tag_index == len(tag_seq) - 1:
        i_tag_index = b_tag_index
        return b_tag_index, i_tag_index  # case when B-LOC at the end of tag_sequence", no I-LOC
    if tag_seq[b_tag_index + 1] == "O":
        i_tag_index = b_tag_index  # case when B-LOC in the middle but no "I-LOC"
        return b_tag_index, i_tag_index
    else:
        for i in range(b_tag_index + 1, len(tag_seq)):
            if tag_seq[i] == i_tag:
                i_tag_index = i  # return index of last I-LOC
        return b_tag_index, i_tag_index


class LongerLocationNer(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    languages = "en"

    def __init__(self, max_outputs=1, seed=0):
        super().__init__(seed, max_outputs=max_outputs)

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
            b_tag_index, i_tag_index = extract_tag_indexes(tag_seq, b_tag, i_tag)
            for _ in range(self.max_outputs):
                token_seq, tag_seq = create_token_and_tag_seq(token_seq, tag_seq, b_tag_index, i_tag_index,
                                                              b_tag, i_tag, self.seed)
                #assert len(token_seq) == len(tag_seq)
                perturbed_sentences.append((token_seq, tag_seq))
                token_seq = token_sequence.copy()
                tag_seq = tag_sequence.copy()
        return perturbed_sentences


# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case
#
#     tf = LongerLocationNer(max_outputs=1)
#     test_cases = []
#     src = ["I am going to New Zealand via Costa Rica .",
#            "I am travelling to London .",
#            "Edison was born in Ohio .",
#            "Michael Jordan is a professor at Berkeley .",
#            "Google head office is located in California ."
#            ]
#     tgt = ["O O O O B-LOC I-LOC O B-LOC I-LOC O",
#            "O O O O B-LOC O",
#            "B-PER O O O B-LOC O",
#            "B-PER I-PER O O O O B-LOC O",
#            "B-ORG O O O O O B-LOC O"
#            ]
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

    # for i, (token_seq, tag_seq) in enumerate(zip(src, tgt)):
    #     tf = LongerLocationNer(max_outputs=1)
    #     print(token_seq, tag_seq)
    #     res = tf.generate(token_seq.split(" "), tag_seq.split(" "))
    #     print(res)
