
from tasks.TaskTypes import TaskType
from interfaces.SentenceOperation import SentenceOperation

from typing import List
from string import punctuation


def generate_subword_and_homophones(word, homophones):
    """ method for generating sub-words of a word if its homophone is not present. This method
    first generate sub-words and that match with their homophones.
    Useful in case of (proper nouns, NERs, rare words Ex: Virat, Quidditch)"""
    index = len(word)//2
    for i in range(index, len(word)):
        f_word=word[:index]
        if f_word.lower() in homophones:
            trans_f_word = homophones[f_word.lower()].title() if f_word.istitle() else homophones[f_word.lower()]
            l_word = word[index:]
            trans_l_word = homophones[l_word] if l_word in homophones else l_word
            return trans_f_word+trans_l_word # returning sub-words homophones
    return word # if no replacement found return input word


def getHomophonicText(sentence, homophones):
    """
    Method for generating transformed sentence with homophone words.
    """
    word_list = sentence.split()
    transformed_word_list = []
    for word in word_list:
        if word in punctuation:
            transformed_word_list.append(word)
        elif word.strip().lower() in homophones:
            # complete word replacement
            trans_word = homophones[word.strip().lower()].title() if word.istitle() \
                else homophones[word.strip().lower()]
            transformed_word_list.append(trans_word)
        else:
            # sub-words replacement
            trans_sub_word = generate_subword_and_homophones(word, homophones)
            transformed_word_list.append(trans_sub_word)
    return " ".join(transformed_word_list)


class HomophonicReplacement(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(
            self,
            seed=0,
            max_outputs=1,
            homophones_file="transformations/homophonic_transformation/homophones.tsv",
            sep="\t",
            encoding="utf-8"
        ):
        super().__init__(seed, max_outputs=max_outputs)
        homophones = {}
        with open(homophones_file, "r", encoding=encoding) as file:
            for line in file:
                key,value = line.strip().split(sep)
                if len(value.split(" ")) >=2:
                    temp = value.split(" ")
                    value = temp[-1].strip()
                homophones[key.strip()] = value.strip()
        self.homophones = homophones

    def generate(self, sentence: str) -> List[str]:
        transformed_sentences = []
        for _ in range(self.max_outputs):
            trans_sent = getHomophonicText(sentence, self.homophones)
            transformed_sentences.append(trans_sent)
        return transformed_sentences


# if __name__ == "__main__":
#     import json
#     from TestRunner import convert_to_snake_case
#
#     tf = HomophonicReplacement()
#     test_cases = []
#     sentence_list = ["Virat Kohli made a big hundred against Australia .",
#                      "The queen Elizabeth II was walking with her cousin .",
#                      "Quidditch is a sport of two teams of seven players each mounted on a broomstick,
#                      played on a hockey rink-sized pitch .",
#                      "The world is a beautiful place .",
#                     ]
#
#     for i, sentence in enumerate(sentence_list):
#         transformed_sentence = tf.generate(sentence)
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence},
#             "outputs": [],
#         })
#         for trans_sentence in transformed_sentence:
#             test_cases[i]["outputs"].append({"sentence":trans_sentence})
#     json_file = {"type": convert_to_snake_case("homophonic_transformation"), "test_cases": test_cases}
#     print(json.dumps(json_file))

    # for sent in sentence_list:
    #     res = tf.generate(sent)
    #     print(sent)
    #     print(res)
    #     print("----")
