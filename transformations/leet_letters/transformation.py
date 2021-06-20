from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Leet speak letter perturbation based on https://simple.wikipedia.org/wiki/Leet, excluding the space > 0.
"""

leet_letter_mappings = {
    "!": "1",
    "7": "1",
    "A": "4",
    "B": "8",
    "C": "0",
    "D": "0",
    "E": "3",
    "G": "6",
    "I": "1",
    "J": "9",
    "L": "7",
    "N": "11",
    "O": "0",
    "S": "5",
    "T": "7",
    "X": "8",
    "Z": "2",
    "b": "6",
    "e": "3",
    "g": "9",
    "h": "4",
    "j": "7",
    "m": "3",
    "o": "0",
    "w": "3",
    "y": "4",
    "|": "1",
    "Θ": "0",
    "ε": "3",
    "ω": "3",
    "∈": "3",
    "∩∩": "3",
}


class LeetLetters(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    def generate(self, sentence: str):
        perturbed = ""
        for letter in sentence:
            perturbed += leet_letter_mappings.get(letter, letter)
        return perturbed
