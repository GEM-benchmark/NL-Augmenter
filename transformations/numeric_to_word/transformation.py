import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def butter_finger(text, prob=0.1, keyboard="querty", seed=0):
    random.seed(seed)
    keyApprox = {}

    if keyboard == "querty":
        keyApprox["q"] = "qwasedzx"
        keyApprox["w"] = "wqesadrfcx"
        keyApprox["e"] = "ewrsfdqazxcvgt"
        keyApprox["r"] = "retdgfwsxcvgt"
        keyApprox["t"] = "tryfhgedcvbnju"
        keyApprox["y"] = "ytugjhrfvbnji"
        keyApprox["u"] = "uyihkjtgbnmlo"
        keyApprox["i"] = "iuojlkyhnmlp"
        keyApprox["o"] = "oipklujm"
        keyApprox["p"] = "plo['ik"

        keyApprox["a"] = "aqszwxwdce"
        keyApprox["s"] = "swxadrfv"
        keyApprox["d"] = "decsfaqgbv"
        keyApprox["f"] = "fdgrvwsxyhn"
        keyApprox["g"] = "gtbfhedcyjn"
        keyApprox["h"] = "hyngjfrvkim"
        keyApprox["j"] = "jhknugtblom"
        keyApprox["k"] = "kjlinyhn"
        keyApprox["l"] = "lokmpujn"

        keyApprox["z"] = "zaxsvde"
        keyApprox["x"] = "xzcsdbvfrewq"
        keyApprox["c"] = "cxvdfzswergb"
        keyApprox["v"] = "vcfbgxdertyn"
        keyApprox["b"] = "bvnghcftyun"
        keyApprox["n"] = "nbmhjvgtuik"
        keyApprox["m"] = "mnkjloik"
        keyApprox[" "] = " "
    else:
        print("Keyboard not supported.")

    probOfTypo = int(prob * 100)

    buttertext = ""
    for letter in text:
        lcletter = letter.lower()
        if not lcletter in keyApprox.keys():
            newletter = lcletter
        else:
            if random.choice(range(0, 100)) <= probOfTypo:
                newletter = random.choice(keyApprox[lcletter])
            else:
                newletter = lcletter
        # go back to original case
        if not lcletter == letter:
            newletter = newletter.upper()
        buttertext += newletter

    return buttertext


"""
Butter Finger implementation borrowed from https://github.com/alexyorke/butter-fingers.
"""


class numeric_to_word(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence: str):
        pertubed = butter_finger(text=sentence, prob=0.05, seed=self.seed)
        return pertubed


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
if __name__ == '__main__':
    import json

    tf = ButterFingersPerturbation()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": {"sentence": tf.generate(sentence)}}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
