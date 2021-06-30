import re
from typing import List

import text_unidecode

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class NormalizeToASCII(SentenceOperation):
    """
    This class offers a method to transform arbitrary text to a suitable ASCII representation.

    Attributes:
        remove_all_non_ascii: Instead of replacing non ASCII characters to a suitable alternative, just remove them.
        language: If the input sentence language is known beforehand, different replacement strategies may be
                  advantageous.
                  Available: de
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = "All"

    def __init__(self, remove_all_non_ascii: bool = False, language: str = "All"):
        super().__init__()
        self.remove_all_non_ascii = remove_all_non_ascii
        self.language = language.lower()

    def generate(self, sentence: str) -> List[str]:
        if self.remove_all_non_ascii:
            sentence = sentence.encode("ascii", "ignore").decode()
        else:
            if self.language == "de":
                umlauts = {
                    "ä": "ae",
                    "Ä": "Ae",
                    "ö": "oe",
                    "Ö": "Oe",
                    "ü": "ue",
                    "Ü": "Ue",
                }
                sentence = re.sub(
                    "[äÄöÖüÜ]",
                    lambda match: umlauts[match.string[match.start() : match.end()]],
                    sentence,
                )
            sentence = text_unidecode.unidecode(sentence)

        return [sentence]
