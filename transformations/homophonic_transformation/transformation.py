from random import choice, sample

from tasks.TaskTypes import TaskType
from interfaces.SentenceOperation import SentenceOperation


def getHomophoneDict():
    homophones = {}
    myfile = open("../homophonic_transformation/homophone_dict.txt", "r")
    for line in myfile:
        word, hmpns = line.strip().split("\t")
        homophones[word] = hmpns.split(" ")
    return homophones


def getRandomHomophonesText(sentence):
    words = sentence.split(" ")
    rand_words = sample(words, min(len(words), 5))
    homophonic_translation = []
    homophone_dict = getHomophoneDict()
    for word in words:
        if word in rand_words:
            homophone = choice(homophone_dict[word]) if word in homophone_dict else word
            homophonic_translation.append(homophone)
        else:
            homophonic_translation.append(word)
    return " ".join(homophonic_translation)


class RandomHomophonicReplacement(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING
    ]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    def generate(self, sentence: str):
        perturbed_sentence = getRandomHomophonesText(sentence)
        return perturbed_sentence


# if __name__ == "__main__":
#     import json
#     from TestRunner import convert_to_snake_case
#
#     tf = RandomHomophonicReplacement()
#     test_cases = []
#     sentence_list = ["The world is a beautiful place .",
#                      "Some children are buying stationary .",
#                      "The queen was walking with her cousin .",
#                      "The prophesy about census was right ."]
#
#     for sentence in sentence_list:
#         transformed_sentence = tf.generate(sentence)
#         test_cases.append({
#             "class": tf.name(),
#             "input": {"sentence": sentence},
#             "output": {"sentence": transformed_sentence}
#         })
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json.dumps(json_file))
