import random
from typing import Dict, List, Tuple

import ftfy
import spacy

from nlaugmenter.common.initialize import spacy_nlp
from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.transformations.replace_financial_amounts import (
    entity_financial_amount,
)

# Token has three keys => text: str, category: str and is_financial_amount: bool
Token = Dict[str, any]


def create_tokens(text: str) -> List[Token]:
    """
    Create a list of tokens that represents the input text.

    Parameters:
        text: The text or sentence to split into tokens.

    Returns:
        List[Token]: a list of tokens modified from Spacy tokens
    """
    text = ftfy.fix_text(text)
    nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
    spacy_tokens = nlp(text)
    return [
        {
            "text": element.text_with_ws,
            "category": "numeric"
            if is_numeric(element.text_with_ws)
            else "other",
            "is_financial_amount": False,
        }
        for element in spacy_tokens
    ]


def is_numeric(text: str) -> bool:
    """
    Determine whether or not a given input text represent a numeric value.

    Parameters:
        text: The input string to analyse.

    Returns:
        bool: Whether the text contains only digits plus dots or commas.
    """
    return text.strip().replace(".", "").replace(",", "").isdigit()


def tag_tokens(tokens: List[Token]) -> List[Token]:
    """
    Determine the type of each tokens in a list of tokens.

    Parameters:
        tokens: Token representation of the sentence to analyse.

    Returns:
        List[Token]: a list of tokens modified from Spacy tokens with their information modified to reflect their type
    """
    counter = 0

    while counter < len(tokens):
        _token_value = tokens[counter]["text"].strip()

        # Verify that the token value corresponds to a currency abbreviation
        if (
            _token_value
            in entity_financial_amount.WORLD_CURRENCY_ABBREVIATIONS
            or _token_value
            in entity_financial_amount.CURRENCIES_WITH_EXCHANGE_RATE_SYMBOLS
        ):

            initial, final = indexes_of_financial_amount(counter, tokens)
            tokens = merge(initial, final, tokens)
        counter += 1

    return tokens


def replace(token: Token, replacement: str):
    """
    Replace the token by another string.

    Parameters:
        token: Token concerned by the replacement.
        replacement: Replacement text.
    """
    if token["text"].endswith(" "):
        token["text"] = replacement.strip(" ") + " "
    else:
        token["text"] = replacement.strip(" ")


def look_ahead_for_amount(
    token_index: int, token_list: List[Token]
) -> Tuple[int, int]:
    """
    Determine if a token or a list of tokens correspond to a financial amount, going forward.

    Parameters:
        token_index: The index to the initial token being a candidate for a financial amount.
        token_list: The list of tokens.

    Returns:
        Tuple[int, int]: The indexes of the initial token and final token being considered for the financial amount.
    """
    # we are going forward
    initial_index, final_index = token_index, token_index
    n_tokens = len(token_list)
    # Format of the financial amount we are looking: $xxx,xxx.xxx
    # The amount could look like ["euros","300"] or ["$","12",".","540"] or ["$", "25",",","000", ".", "00"]
    if (
        (
            token_index != n_tokens - 2
            and token_list[token_index + 2]["text"].strip() == ","
        )
        and (
            token_index != n_tokens - 3
            and is_numeric_token(token_list[token_index + 3], 3)
        )
        and (
            token_index != n_tokens - 4
            and token_list[token_index + 4]["text"].strip() == "."
        )
        and (
            token_index != n_tokens - 5
            and token_list[token_index + 5]["category"] == "numeric"
        )
    ):
        final_index = token_index + 5
    # Format of the financial amount we are looking: $xxx,xxx or $xxx.xxx
    # It should look like ["$","12",".","540"] or ["$","12",",","540"]
    elif token_index != n_tokens - 2 and (
        token_list[token_index + 2]["text"].strip() == "."
        or token_list[token_index + 2]["text"].strip() == ","
    ):
        if (
            token_index != n_tokens - 3
            and token_list[token_index + 3]["category"] == "numeric"
        ):
            final_index = token_index + 3
        else:
            final_index = token_index + 1
    # Format of the financial amount we are looking: $ xx xxx
    # The amount should look like ["$","12","540"]
    elif (token_index != n_tokens - 2) and (
        token_list[token_index + 2]["category"] == "numeric"
    ):
        final_index = token_index + 2
    # Format of the financial amount we are looking: $ x{1,n}
    else:
        final_index = token_index + 1

    # Special case where there is 2 symbols, e.g. ["$", "12", "USD"]
    if (final_index != n_tokens - 1) and (
        (
            token_list[final_index + 1]["text"].strip()
            in entity_financial_amount.WORLD_CURRENCY_ABBREVIATIONS
        )
        or (
            token_list[final_index + 1]["text"].strip()
            in entity_financial_amount.CURRENCIES_WITH_EXCHANGE_RATE_SYMBOLS
        )
    ):
        final_index = final_index + 1
    return initial_index, final_index


def look_backward_for_amount(
    token_index: int, token_list: List[Token]
) -> Tuple[int, int]:
    """
    Determine if a token or a list of tokens correspond to a financial amount, going backward.

    Parameters:
        token_index: The index to the final token being a candidate for a financial amount.
        token_list: The list of tokens.

    Returns:
        Tuple[int, int]: The indexes of the initial token and final token being considered for the financial amount.
    """
    # We are going backward

    initial_index, final_index = token_index, token_index
    #  Format of the financial amount we are looking: format xxx,xxx.xxx$
    # The amount could look like ["300","euros"] or ["12",".","540","$"] or ["25",",","000", ".", "00", "$"]
    if (
        (
            token_index != 1
            and token_list[token_index - 2]["text"].strip() == "."
        )
        and (
            token_index != 2
            and is_numeric_token(token_list[token_index - 3], 3)
        )
        and (
            token_index != 3
            and token_list[token_index - 4]["text"].strip() == ","
        )
        and (
            token_index != 4
            and token_list[token_index - 5]["category"] == "numeric"
        )
    ):
        initial_index = token_index - 5
    # Format of the financial amount we are looking: xxx,xxx$ or xxx.xxx$
    # The amount should look like ["12",".","540","$"] or ["12",",","540","$"]
    elif token_index != 1 and (
        token_list[token_index - 2]["text"].strip() == "."
        or token_list[token_index - 2]["text"].strip() == ","
    ):
        if (
            token_index != 2
            and token_list[token_index - 3]["category"] == "numeric"
        ):
            initial_index = token_index - 3
        else:
            initial_index = token_index - 1
    # Format of the financial amount we are looking: 12 540$
    # The amount should look like ["12","540","$"]
    elif (
        token_index != 1
        and token_list[token_index - 2]["category"] == "numeric"
    ):
        initial_index = token_index - 2
    # Format of the financial amount we are looking: xxxxx{1,n} $
    else:
        initial_index = token_index - 1
    # Special case where there is 2 symbols, e.g. ["12","$","USD"]
    if token_index != len(token_list) - 1 and (
        (
            token_list[token_index + 1]["text"].strip()
            in entity_financial_amount.WORLD_CURRENCY_ABBREVIATIONS
            + entity_financial_amount.CURRENCIES_WITH_EXCHANGE_RATE_SYMBOLS
        )
    ):
        final_index = token_index + 1
    return initial_index, final_index


def is_numeric_token(token: Token, expected_length: int or None) -> bool:
    """
    Determine whether a given token is a numeric token of the certain length.

    Parameters:
        token: Token to be checked.
        expected_length: The shape (number of digit) the token is expected to be.

    Returns:
        bool: Whether the token is_numeric and matches a specific length
    """
    if expected_length is None:
        return token["category"] == "numeric"
    else:
        return (
            token["category"] == "numeric"
            and len(token["text"].strip()) == expected_length
        )


def generate_financial_amount_replacement(
    token: Token,
    financial_amounts_encountered: Dict,
    percentage_financial_amount_variation: int,
) -> Tuple[str, Dict]:
    """
    Generate replacements for an amount and currency based on previous amounts generated to
    conserve coherence within document.

    Parameters:
        token: The financial amount token for which a replacement is generated.
        financial_amounts_encountered: The dictionary of currency and amounts already encountered.
        percentage_financial_amount_variation: The variation applied when generating the amount.

    Returns:
          Tuple[str, Dict]: The financial amount generated and the updates dict of financial_amounts_encountered
    """
    amount, currency = entity_financial_amount.get_amount_and_currency(
        token["text"].strip()
    )
    # case currency with conversion rate
    if (
        "name" in currency.keys()
    ):  # only currencies with conversion rate have a name
        # case currency has already been encountered in the text previously
        if currency["name"] in financial_amounts_encountered.keys():
            for replaced_amount, new_amount in financial_amounts_encountered[
                currency["name"]
            ]["amounts"]:
                # case amount has already been encountered in the text previously
                if amount == replaced_amount:
                    return (
                        new_amount,
                        financial_amounts_encountered,
                    )

            currency_to_generate = financial_amounts_encountered[
                currency["name"]
            ]["name"]
            currency_to_generate = (
                entity_financial_amount.CURRENCIES_WITH_EXCHANGE_RATE[
                    currency_to_generate
                ]
            )
            new_financial_amount = entity_financial_amount.generate_financial_amount_for_specific_currency(
                amount,
                currency,
                currency_to_generate,
                financial_amounts_encountered[currency["name"]][
                    "symbol_chosen"
                ],
                percentage_financial_amount_variation,
            )

            if len(token["text"].split(" ")) > 1:
                new_financial_amount += " "

            financial_amounts_encountered[currency["name"]]["amounts"].append(
                (amount, new_financial_amount)
            )
        else:
            # case currency has never been encountered in the text previously
            currencies_generated = [
                financial_amounts_encountered[_c]["name"]
                for _c in financial_amounts_encountered
            ]
            (
                new_financial_amount,
                new_currency,
                new_symbol,
            ) = entity_financial_amount.generate_financial_amount_for_currency_with_exchange_rate(
                amount,
                currency,
                currencies_generated,
                percentage_financial_amount_variation,
            )

            if len(token["text"].split(" ")) > 1:
                new_financial_amount += " "

            financial_amounts_encountered[currency["name"]] = {
                "name": new_currency["name"],
                "symbol_chosen": new_symbol,
                "amounts": [(amount, new_financial_amount)],
            }

        return new_financial_amount, financial_amounts_encountered
    # case currency has no associated conversion rate: just replace the financial amount
    return (
        entity_financial_amount.generate_new_format(
            entity_financial_amount.generate_new_amount(
                amount, percentage_financial_amount_variation
            ),
            currency["symbol"][0],
        ),
        financial_amounts_encountered,
    )


class ReplaceFinancialAmount(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "possible-meaning-alteration",
        "high-precision",
        "high-coverage",
    ]

    def __init__(self, seed: int = 0, max_outputs: int = 1) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        # we seed the random generator to keep coherent and consistent transformation throughout a text.
        random.seed(self.seed)

        percentage_financial_amount_variation = random.choice(
            [-1, 1]
        ) * random.randint(1, 20)
        financial_amounts_encountered = {}

        token_list = create_tokens(sentence)
        tagged_tokens = tag_tokens(token_list)

        for _token in tagged_tokens:
            if _token["is_financial_amount"]:
                (
                    replacement,
                    financial_amounts_encountered,
                ) = generate_financial_amount_replacement(
                    _token,
                    financial_amounts_encountered,
                    percentage_financial_amount_variation,
                )
                replace(_token, replacement)

        result = "".join(_token["text"] for _token in tagged_tokens)

        if self.verbose:
            print(f"Perturbed Input from {sentence} : {result}")

        return [result]


def indexes_of_financial_amount(
    token_index: int, token_list: List
) -> Tuple[int, int]:
    """
    Search for the initial and final token indexes of a financial amount in a list of tokens.

    Parameters:
        token_list: Token representation of the sentence to analyse.
        token_index: index from which to search for financial amount.

    Returns:
        Tuple[int, int]: The indexes of the initial token and final token being considered for the financial amount.
    """
    initial_index, final_index = token_index, token_index
    # we test if we should go backward or forward to search for the amount
    # case forward, the currency symbol is after the amount: `15 $`
    if (
        token_index != 0
        and token_list[token_index - 1]["category"] == "numeric"
    ):
        initial_index, final_index = look_backward_for_amount(
            token_index, token_list
        )

    # case backward, the currency symbol is before the amount: `USD 15`
    elif (
        token_index != len(token_list) - 1
        and token_list[token_index + 1]["category"] == "numeric"
    ):
        initial_index, final_index = look_ahead_for_amount(
            token_index, token_list
        )

    return initial_index, final_index


def merge(
    initial_index: int, final_index: int, token_list: List[Token]
) -> List[Token]:
    """
    Merge the tokens identified as financial amount into a unique token tagged accordingly.

    Parameters:
        token_list: Token representation of the sentence to analyse.
        initial_index: starting index of identified financial amount.
        final_index: ending index of identified financial amount.

    Returns:
        List[Token]: The updated list of tokens
    """
    # The token is just a currency symbol not followed by any numbers
    if initial_index == final_index:
        return token_list

    # Update the token list and value with the financial amount token identified
    value = "".join(
        [
            _token["text"]
            for _token in token_list[initial_index : final_index + 1]
        ]
    )
    new_token: Token = {
        "text": value,
        "is_financial_amount": True,
        "category": "other",
    }
    new_token_list = (
        token_list[:initial_index]
        + [new_token]
        + token_list[final_index + 1 :]
    )
    return new_token_list
