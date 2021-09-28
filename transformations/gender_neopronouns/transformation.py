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
    keywords = [
        "lexical",
        "model-based",
        "tokenizer-required",
        "highly-meaning-preserving",
        "high-coverage",
    ]

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
        Generate neopronoun substitution on `sentence`.

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
            children = list(token.children)

            if token.pos_ == "PRON" and token.text.lower() not in ["i", "my"]:
                if "Case" in morph and "Reflex" in morph:
                    pron_type = "REF"
                elif "Case" in morph and morph["Case"] == "Nom":
                    pron_type = "NOM"
                elif "Case" in morph and morph["Case"] == "Acc":
                    pron_type = "ACC"
                elif "Poss" in morph and morph["Poss"] == "Yes":
                    if token.text.lower() in [
                        "mine",
                        "yours",
                        "his",
                        "hers",
                        "its",
                    ]:
                        pron_type = "PRED"
                    else:
                        pron_type = "PRNOM"
                elif token.tag_ == "PRP":
                    pron_type = "NOM"
                else:
                    pron_type = token.tag_

                # try-catch to handle case when `token.tag_` is index
                try:
                    neopronoun = TAGS[self.swap_neopronoun][pron_type]
                    neopronoun = (
                        neopronoun.capitalize()
                        if token.is_title
                        else neopronoun.lower()
                    )
                    pieces.append(neopronoun)
                except KeyError:
                    pieces.append(token.text)

            # handle third person singular -s cases
            elif (
                children and token.tag_ == "VBZ" and children[0].pos_ == "PRON"
            ):
                pieces.append(token.lemma_)

            else:
                if token.is_punct and token.is_sent_end:
                    pieces[-1] += token.text
                else:
                    pieces.append(token.text)

        return [" ".join(pieces)]
