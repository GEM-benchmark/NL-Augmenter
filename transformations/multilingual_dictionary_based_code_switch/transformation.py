import os
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

CURRENT_FILE_ROOT = os.path.dirname(os.path.realpath(__file__))

"""
The bilingual dict code-switch method used here comes from paper "Word Translation Without Parallel Data" MUSE
We utilize all language from this bilingual dictionary in default. 
link: https://arxiv.org/abs/1710.04087
"""

def load_dict():
    dict_path = os.path.join(CURRENT_FILE_ROOT, "dict")
    languages = [
        "de",
        "it",
        "zh",
        "jp",
        "ru",
        "es",
        "fr",
        "th",
        "eu",
        "ca",
        "el",
        "bg",
        "tr",
        "ar",
        "vi",
        "hi",
        "sw",
        "ur",
    ]
    switch_dict = []
    for language in languages:
        switch_dict.append(dict())
        with open(
            os.path.join(dict_path, language + ".txt"), "r", encoding="utf-8"
        ) as f:
            for pair in f.readlines():
                pair = pair.strip()
                try:
                    src, tgt = pair.split("\t")
                except:
                    src, tgt = pair.split(" ")
                if src not in switch_dict[-1]:
                    switch_dict[-1][src] = [tgt]
                else:
                    switch_dict[-1][src].append(tgt)
    return switch_dict


"""
Code switch method. From paper "CoSDA-ML: Multi-Lingual Code-Switching Data Augmentation for Zero-Shot Cross-Lingual NLP"
link: https://arxiv.org/abs/2006.06402
"""


def code_switch(sentence, switch_dict, code_switch_rate, seed):
    random.seed(seed)
    words = sentence.split(" ")
    out = ""
    for word in words:
        language = random.randint(0, len(switch_dict) - 1)
        if (
            word in switch_dict[language]
            and code_switch_rate >= random.random()
        ):
            out += switch_dict[language][word][
                random.randint(0, len(switch_dict[language][word]) - 1)
            ]
            out += " "
        else:
            out += word + " "
    return out.strip()


class MultilingualDictionaryBasedCodeSwitch(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.SENTIMENT_ANALYSIS,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1, code_switch_rate=0.9):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.code_switch_rate = code_switch_rate
        self.switch_dict = load_dict()

    def generate(self, sentence: str):

        return [code_switch(sentence, self.switch_dict, self.code_switch_rate, self.seed)]


if __name__ == "__main__":
    import json
    sc = MultilingualDictionaryBasedCodeSwitch()
    with open("test.json", "r") as f:
        data = json.load(f)
    new_data = []
    for data_item in data['test_cases']:
        data_item['outputs'][0]['sentence'] = sc.generate(data_item['inputs']['sentence'])[0]
        new_data.append(data_item)
    data['test_cases'] = new_data

    with open("test.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
