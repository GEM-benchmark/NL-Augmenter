from typing import List, Tuple, Set
from initialize import spacy_nlp
import random
import spacy
import ftfy
import os

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def load(path_to_file: str) -> List[List[str]]:
    """
    Load from a file, the list of abbreviations as tuple(list) of the expanded and the contracted form.

    Parameters:
        `path_to_file`: Path to file containing the abbreviations.
        The file should contains one abbreviation pair per line, separated by a semicolon. e.g.: ACCT:account.
    Returns:
        List of pairs of contracted and expanded abbreviations.
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(
        os.path.join(__location__, path_to_file), "r", encoding="utf-8"
    ) as _file:
        content = _file.read()
        line = content.split("\n")

    if line[-1] == "":
        line = line[:-1]

    return [element.split(":", 1) for element in line]


def separate_into_contracted_and_expanded_form(
    abbreviations: List,
) -> Tuple[List, List]:
    """
    Split a given list of abbreviations pairs into two lists.
    One for contracted form and the other for expanded form.
    The abbreviation list has the form ACCT:account.

    Parameters:
        `abbreviations`: A list of pairs of contracted and expanded abbreviations.
    Returns:
        A Tuple of two lists.
    """
    contracted_abbreviations = []
    expanded_abbreviations = []

    for contracted_form, expanded_form in abbreviations:
        contracted_abbreviations.append(contracted_form.lower())
        expanded_abbreviations.append(expanded_form.lower())
    return contracted_abbreviations, expanded_abbreviations


def create_tokens(text: str) -> List:
    """
    Create a list of tokens that represents the input text.

    Parameters:
        `text`: The text to transform into token list.
    Returns:
        A list of tokens.
    """
    text = ftfy.fix_text(text)
    nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
    spacy_tokens = nlp(text)
    return [
        {
            "text": element.text,
            "is_a_verb": element.tag_ is not None
            and element.tag_.startswith("V"),
            "end_space": " " if element.text_with_ws.endswith(" ") else "",
            "is_abbreviation": False,
            "is_expanded_abbreviation": False,
        }
        for element in spacy_tokens
    ]


def identify_init_and_end_of_expanded_abbreviations(
    tokens: List, abbreviation: str
) -> Tuple[int, int]:
    """
    Look for init and end token indexes matching an expanded abbreviation.
    Return -1, -1 if the abbreviation was not found.
    ```
    tokens = [{"text": "as", ...}, {"text": "soon", ...}, {"text": "as", ...}, {"text": "possible", ...}, {"text": "do", ...}]
    abbreviation = "as soon as possible"
    (0, 3) = identify_init_and_end_of_expanded_abbreviations(tokens, abbreviation)
    ```

    Parameters:
        `tokens`: The list of tokens representing a sentence.
        `abbreviation`: The abbreviation string to search for in the list of tokens.
    Returns:
        The first and last index of abbreviation if found in the token list.
    """
    candidate_abbreviation: str = ""
    for i, token in enumerate(tokens):
        candidate_abbreviation = (
            candidate_abbreviation + token["text"] + token["end_space"]
        )
        if candidate_abbreviation.lower().strip() == abbreviation.lower():
            return 0, i
        if candidate_abbreviation.lower() in abbreviation.lower():
            continue
        else:
            return -1, -1
    return -1, -1


def fuse_token_values_for_expanded_abbreviations(
    tokens: List, merge_collection: Set[Tuple[int, int]]
) -> List:
    """
    Fuse token values for tokens that have been identified as expanded abbreviations into a single token.
    Ex: `[{'text' : 'as'}, {'text' : 'soon'}, {'text' : 'as'}, {'text' : 'possible'}]` =>
    `[{'text' : 'as soon as possible'}]`.

    Parameters:
        `tokens`: The list of tokens representing a sentence.
        `merge_collection`: List of `start` and `finish` indexes.
            `start`: The first index of identified abbreviation.
            `finish`: The last index of identified abbreviation.
    Returns:
        A list of tokens with expanded abbreviation tokens fused.
    """
    start_indexes = [start for start, _ in merge_collection]
    new_tokens = []
    counter = 0
    while counter < len(tokens):
        if counter not in start_indexes:
            new_tokens.append(tokens[counter])
            counter += 1
            continue

        finish = [
            finish for start, finish in merge_collection if start == counter
        ][0]

        if finish - counter == 0:
            tokens[counter]["is_abbreviation"] = True
            tokens[counter]["is_expanded_abbreviation"] = True
            new_tokens.append(tokens[counter])
            counter += 1
            continue

        new_token_text = {}

        text = "".join(
            [
                token["text"] + token["end_space"]
                for token in tokens[counter : finish + 1]
            ]
        )
        new_token_text["text"] = text.strip()
        new_token_text["end_space"] = tokens[finish]["end_space"]
        new_token_text["is_abbreviation"] = True
        new_token_text["is_expanded_abbreviation"] = True

        new_tokens.append(new_token_text)
        counter = finish + 1

    return new_tokens


class ReplaceAbbreviations(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "highly-meaning-preserving",
        "high-precision",
        "high-coverage",
        "low-generations",
        "domain-knowledge",
        "world-knowledge",
    ]

    def __init__(
        self,
        seed: int = 0,
        max_outputs: int = 1,
    ) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.abbreviations = load("abbreviations.txt")
        (
            self.contracted_abbreviations,
            self.expanded_abbreviations,
        ) = separate_into_contracted_and_expanded_form(self.abbreviations)

    def tag_tokens(self, tokens: List) -> List:
        """
        Iterate over all tokens and tags tokens that correspond to contracted or expanded abbreviations.

        Parameters:
            `tokens`: The list of tokens representing a sentence.
        Returns:
            The list of tokens with abbreviation token(s) tagged.
        """
        counter = 0
        merge_collection = set()
        # loop over token in list looking for abbreviation to tag.
        while counter < len(tokens):
            token = tokens[counter]
            # skip when the token represent a verb
            if token["is_a_verb"]:
                counter += 1
                continue
            # tag when a contracted abbreviation is detected
            if token["text"].lower() in self.contracted_abbreviations:
                tokens[counter]["is_abbreviation"] = True
                counter += 1
                continue
            # case of expanded abbreviation
            # find all abbreviations that start with the current token
            # ex: if current token is "as", will selected "as soon as possible".
            candidate_abbreviations = [
                abbr
                for abbr in self.expanded_abbreviations
                if abbr.startswith(token["text"].lower() + token["end_space"])
            ]
            for candidate_abbreviation in candidate_abbreviations:
                # search for the candidate abbreviation in the rest of the token list.
                (
                    start,
                    finish,
                ) = identify_init_and_end_of_expanded_abbreviations(
                    tokens[counter:], candidate_abbreviation
                )
                if start == -1 and finish == -1:  # case abbreviation not found
                    continue
                else:  # abbreviation found, add it to the merge set
                    merge_collection.add((start + counter, finish + counter))
                    counter += finish
                    break
            counter += 1

        # merge all found expanded abbreviation and tag them as abbreviation
        tokens = fuse_token_values_for_expanded_abbreviations(
            tokens, merge_collection
        )
        for t in tokens:
            print(t)
        return tokens

    def replace_abbreviation(self, token):
        """
        Replace the input token with its contracted form it is an expanded one, or with its expanded one otherwise.

        Parameters:
            `token`: a representation of one unit of the sentence (a word, a punctuation, an abbreviation...).
        """
        if token["is_abbreviation"] and not token["is_expanded_abbreviation"]:
            replacement = [
                position[1]
                for position in self.abbreviations
                if position[0].lower() == token["text"].lower()
            ][0]
            token["text"] = replacement.lower()
        else:
            replacement = [
                position[0]
                for position in self.abbreviations
                if position[1].lower() == token["text"].lower()
            ][0]
            token["text"] = replacement

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)

        tokens = create_tokens(sentence)
        tagged_tokens = self.tag_tokens(tokens)

        tokens_to_replace = []

        abbreviation_tokens = [
            _token for _token in tagged_tokens if _token["is_abbreviation"]
        ]

        if abbreviation_tokens:
            number_of_token_replaced = random.randint(
                1, len(abbreviation_tokens)
            )
            tokens_to_replace = random.sample(
                abbreviation_tokens, number_of_token_replaced
            )

        for _token in tokens_to_replace:
            self.replace_abbreviation(_token)

        result = "".join(
            _token["text"] + _token["end_space"] for _token in tagged_tokens
        )

        if self.verbose:
            print(f"Perturbed Input from {sentence} : {result}")

        return [result]
