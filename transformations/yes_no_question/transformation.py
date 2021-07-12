import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def butter_finger(text, prob=0.1, keyboard="querty", seed=0, max_outputs=1):
    random.seed(seed)
    key_approx = {}

    if keyboard == "querty":
        key_approx["q"] = "qwasedzx"
        key_approx["w"] = "wqesadrfcx"
        key_approx["e"] = "ewrsfdqazxcvgt"
        key_approx["r"] = "retdgfwsxcvgt"
        key_approx["t"] = "tryfhgedcvbnju"
        key_approx["y"] = "ytugjhrfvbnji"
        key_approx["u"] = "uyihkjtgbnmlo"
        key_approx["i"] = "iuojlkyhnmlp"
        key_approx["o"] = "oipklujm"
        key_approx["p"] = "plo['ik"

        key_approx["a"] = "aqszwxwdce"
        key_approx["s"] = "swxadrfv"
        key_approx["d"] = "decsfaqgbv"
        key_approx["f"] = "fdgrvwsxyhn"
        key_approx["g"] = "gtbfhedcyjn"
        key_approx["h"] = "hyngjfrvkim"
        key_approx["j"] = "jhknugtblom"
        key_approx["k"] = "kjlinyhn"
        key_approx["l"] = "lokmpujn"

        key_approx["z"] = "zaxsvde"
        key_approx["x"] = "xzcsdbvfrewq"
        key_approx["c"] = "cxvdfzswergb"
        key_approx["v"] = "vcfbgxdertyn"
        key_approx["b"] = "bvnghcftyun"
        key_approx["n"] = "nbmhjvgtuik"
        key_approx["m"] = "mnkjloik"
        key_approx[" "] = " "
    else:
        print("Keyboard not supported.")

    prob_of_typo = int(prob * 100)
    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for letter in text:
            lcletter = letter.lower()
            if lcletter not in key_approx.keys():
                new_letter = lcletter
            else:
                if random.choice(range(0, 100)) <= prob_of_typo:
                    new_letter = random.choice(key_approx[lcletter])
                else:
                    new_letter = lcletter
            # go back to original case
            if not lcletter == letter:
                new_letter = new_letter.upper()
            butter_text += new_letter
        perturbed_texts.append(butter_text)
    return perturbed_texts


"""
Butter Finger implementation borrowed from https://github.com/alexyorke/butter-fingers.
"""


class ButterFingersPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        perturbed_texts = butter_finger(
            text=sentence,
            prob=0.05,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = ButterFingersPerturbation(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
