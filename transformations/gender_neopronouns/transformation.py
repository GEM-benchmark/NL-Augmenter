from typing import List

import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from .constants import TAGS


class GenderNeoPronouns(SentenceOperation):
    """[summary]

    Args:
        SentenceOperation ([type]): [description]

    """

    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        swap_neopronoun: str = "they",
        seed: int = 0,
        verbose: bool = False,
        max_outputs: int = 1,
    ) -> None:
        assert (
            swap_neopronoun.capitalize() in TAGS
        ), f"swap_neopronoun can only have value of {TAGS.keys()}"
        self.nlp = spacy.load("en_core_web_sm")
        self.swap_neopronoun = swap_neopronoun
        super().__init__(seed=seed, verbose=verbose, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        doc = self.nlp(sentence)
        pieces = []
        for token in doc:
            morph = token.morph.to_dict()
            if token.pos_ == "PRON":
                if "Case" in morph:
                    pron_type = morph["Case"].upper()
                elif "Poss" in morph:
                    pron_type = morph["PronType"].upper()
                else:
                    pron_type = "ACC"

                try:
                    neopronoun = TAGS[self.swap_neopronoun][pron_type]
                    neopronoun = (
                        neopronoun.capitalize()
                        if token.is_title
                        else neopronoun.lower()
                    )
                    pieces.append(neopronoun)
                except Exception:
                    pieces.append(token.text)
            else:
                # NOTE: find a more elegant solution to tokenizing punctuations.
                if token.is_punct:
                    pieces[-1] += token.text
                else:
                    pieces.append(token.text)

        return [" ".join(pieces)]
