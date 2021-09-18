import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Modify date formats with perturbations.
"""



class WordsToNumbers(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]

    def __init__(self, seed: int = 0) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)


    def generate(self, sentence: str) -> List[str]:
        # Adapted from
#       # https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
        #

        # Segment the number from the rest of the sentence
        # Split by space
        # If there's a hyphen, split
        # If there's an and, split

    def text2int(textnum, numwords={}):
        if not numwords:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):
                numwords[word] = (1, idx)
            for idx, word in enumerate(tens):
                numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales):
                numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        for word in textnum.split():
            if word not in numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current

    print
    text2int("seven billion one hundred million thirty one thousand three hundred thirty seven")
