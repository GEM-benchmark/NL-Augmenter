import itertools
import random
import re

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from neuspell import BertChecker 
# TODO remember to add neuspell to requirements.txt

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

def modified_butter_finger(text, prob=0.1, keyboard="querty", seed=0, 
        max_outputs=1):
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
        key_approx["p"] = "ploik"

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

def spelling_mis_correction(text, checker, prob=0.5, seed=0, max_outputs=1):
    random.seed(seed)

    corrected_texts = []
    # First, remove special characters to avoid most alignment issues
    text = re.sub('[^A-Za-z]+', ' ', text)

    # Call modified butter finger to perturb text
    perturbed_texts = modified_butter_finger(text, prob=prob, 
            seed=seed, max_outputs=max_outputs)
    for perturbed_text in perturbed_texts:
        # Call neural spelling correction API
        corrected_text = checker.correct(perturbed_text)
        # Remove perturbed and not-corrected text
        original_words = text.split()
        perturbed_words = perturbed_text.split()
        corrected_words = corrected_text.split()
        for i in range(min(len(original_words), len(corrected_words))):
            if corrected_words[i] == perturbed_words[i]:
                corrected_words[i] = original_words[i]
        corrected_text = " ".join(corrected_words)
        corrected_texts.append(corrected_text)
        
    return corrected_texts


class SpellingMisCorrection(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION, # TODO add which tasks are relevant 
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.checker = BertChecker()
        self.checker.from_pretrained()

    def generate(self, sentence: str):
        corrected_texts = spelling_mis_correction(
            text=sentence,
            checker=self.checker,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return corrected_texts
