import random

from interfaces.SentenceTransformation import SentenceTransformation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def butter_finger(text, prob=0.1, keyboard='querty', seed=0):
    random.seed(seed)
    keyApprox = {}

    if keyboard == "querty":
        keyApprox['q'] = "qwasedzx"
        keyApprox['w'] = "wqesadrfcx"
        keyApprox['e'] = "ewrsfdqazxcvgt"
        keyApprox['r'] = "retdgfwsxcvgt"
        keyApprox['t'] = "tryfhgedcvbnju"
        keyApprox['y'] = "ytugjhrfvbnji"
        keyApprox['u'] = "uyihkjtgbnmlo"
        keyApprox['i'] = "iuojlkyhnmlp"
        keyApprox['o'] = "oipklujm"
        keyApprox['p'] = "plo['ik"

        keyApprox['a'] = "aqszwxwdce"
        keyApprox['s'] = "swxadrfv"
        keyApprox['d'] = "decsfaqgbv"
        keyApprox['f'] = "fdgrvwsxyhn"
        keyApprox['g'] = "gtbfhedcyjn"
        keyApprox['h'] = "hyngjfrvkim"
        keyApprox['j'] = "jhknugtblom"
        keyApprox['k'] = "kjlinyhn"
        keyApprox['l'] = "lokmpujn"

        keyApprox['z'] = "zaxsvde"
        keyApprox['x'] = "xzcsdbvfrewq"
        keyApprox['c'] = "cxvdfzswergb"
        keyApprox['v'] = "vcfbgxdertyn"
        keyApprox['b'] = "bvnghcftyun"
        keyApprox['n'] = "nbmhjvgtuik"
        keyApprox['m'] = "mnkjloik"
        keyApprox[' '] = " "
    else:
        print("Keyboard not supported.")

    probOfTypoArray = []
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


class ButterFingersPerturbation(SentenceTransformation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    locales = ["en"]

    def __init__(self):
        super().__init__()

    def generate(self, sentence: str):
        pertubed = butter_finger(text=sentence, prob=0.05)
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed
