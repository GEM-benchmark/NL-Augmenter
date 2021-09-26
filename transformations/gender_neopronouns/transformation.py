from typing import List

import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from .constants import TAGS


class GenderNeoPronouns(SentenceOperation):
    """This transformation performs **_grammatically correct substitution_**
    of the gendered pronouns he/she in a given sentence with their
    neopronoun counterparts.
    """

    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self,
        swap_neopronoun: str = "They",
        seed: int = 0,
        verbose: bool = False,
        max_outputs: int = 1,
    ) -> None:
        """
        Args:
            swap_neopronoun:
                The neopronoun to swap: Defaults to "They".
                Must be one of
                [
                    'Ae', 'Co', 'E', 'Ey', 'Fae', 'He', 'Hu', 'Ne',
                    'Per', 'Person', 'She', 'They', 'Thon',
                    'Ve', 'Vi', 'Xe', 'Ze'
                ]
            seed:
                Random seed. Defaults to 0.
            verbose:
                verbosity level. Defaults to False.
            max_outputs:
                NotImplemented always generate 1 output
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.swap_neopronoun = swap_neopronoun.capitalize()
        # ensure swap_neopronoun exists in TAGS
        assert (
            self.swap_neopronoun in TAGS
        ), f"swap_neopronoun can only have value of {TAGS.keys()}"

        super().__init__(seed=seed, verbose=verbose, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        """
        Args:
            sentence:
                The input sentence to be transformed
        Returns:
            The transformed sentence
        """
        doc = self.nlp(sentence)
        pieces = []
        for token in doc:
            morph = token.morph.to_dict()
            child = next(token.children, spacy.tokens.Token)

            if token.pos_ == "PRON":
                if "Case" in morph and "Reflex" in morph:
                    pron_type = "REF"
                elif "Case" in morph:
                    pron_type = morph["Case"].upper()
                elif token.tag_ == 'PRP$':
                    pron_type = 'PRS'
                elif token.tag_ == 'PRP':
                    pron_type = 'PRP'
                else:
                    pron_type = token.tag_

                # handle case when using `token.tag_` as index
                try:
                    neopronoun = TAGS[self.swap_neopronoun][pron_type]
                    neopronoun = (
                        neopronoun.capitalize()
                        if token.is_title
                        else neopronoun.lower()
                    )
                    pieces.append(neopronoun)
                except ValueError:
                    pieces.append(token.text)

            # handle third person singular -s cases
            elif token.tag_ == 'VBZ' and child.pos_ == 'PRON':
                pieces.append(token.lemma_)

            else:
                # NOTE: find a more elegant solution to tokenizing punctuations.
                if token.is_punct and len(pieces) != 0:
                    pieces[-1] += token.text
                else:
                    pieces.append(token.text)

        return [" ".join(pieces)]
