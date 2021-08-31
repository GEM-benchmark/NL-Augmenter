


import random

from typing import List
from checklist.editor import Editor

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

def german_nouns(text, german_pairs):
    for name in german_pairs.keys():
        if name in text:
            text = text.replace(name, german_pairs[name])
    return text 
german_pairs = {
    "der Artz": "dir Ärztin",
    "der Vater": "die Mutter",
    "der Stiefsohn": "die Stieftochter",
    "der Herzog": "die Herzogin",
    "der Zauberer": "die Hexe",
    "der Baron": "die Baronin",
    "der Prinz": "die Prinzessin",
    "der Schwiegersohn": "der Schwiegersohn",
    "der Herzog": "die Herzogin",
    "der freund": "die freundin",
    "der Onkel": "die Tante",
    "der Jäger": "die Jägerin",
    "der Meister": "die Herrin",
    "der Großvater": "die Oma",
    "das Mädchen": "der Junge",
    "der Mann": "die Frau",
    "der Priester": "die Priesterin",
    "der Mönch": "die Nonne",
    "der Gott": "die Göttin",
    "der Steward": "der Stewardess",
    "der Mord": "die Mörderin",
    "der Kellner": "die Kellnerin",
    "der Kaiser": "die Kaiserin",
    "der König": "die Königin",
    "Ehemann":"Frau",
    "der Stiefvater": "die Stiefmutter",
    "der Sohn": "die Tochter",
    "der Geschäftsmann": "die Geschäftsfrau",
    "der Witwer": "die Witwe",
    "der Schauspieler": "die Schauspielerin",
    "der Krankenpfleger": "die Krankenschwester",
    "der Schreiber": "die Schreiberin",
    "der Patensohn": "die Patentochter",
    "der Pate": "die Patin",
    "der Techniker": "die Technikerin",
    "der Ingenieur": "die Ingenieurin",
    "der Fahrer": "die Fahrerin",
    "der Chirurg": "die Chirurgin",
    "der Mechaniker": "die Mechanikerin"

}
class GermanGenderSwap(SentenceOperation):

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["de"]

    def __init__(
        self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs)
        self.german_pairs = german_pairs

        
    def generate(self, sentence: str):
        return [german_nouns(sentence, self.german_pairs)]


"""
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = GermanGenderSwap(max_outputs=1)
    test_cases = []
    for sentence in ["der Arzt arbeitet.",
                     "der ingenieur geht.",
                     "die Mutter hat dich gesegnet",
                     "der Fensterer trauert",
                     "der Mann ist weg"]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))
"""