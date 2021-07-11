import itertools
import random
import re

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

# Setting up a tuple of possible replaceable greetings and farewells
GREETINGS = (
    "Hi",
    "Hello",
    "Hey",
    "Howdy",
    "Greetings",
    "Good morning",
    "Good afternoon",
    "Good evening",
    "What's up",
    "Sup",
)

# Creating a tuple of sentences that can't be simply replaced by a short greeting
SPECIAL_GREETINGS = (
    "It's nice to meet you.",
    "It's great to meet you.",
    "Pleased to meet you.",
    "How are you?",
    "How are you doing?",
    "How is it going on?",
    "How is it going?",
)

FAREWELLS = (
    "Goodbye",
    "Bye bye",
    "Bye",
    "See you soon",
    "See you",
    "See ya",
    "Best regards",
    "Have a nice day",
    "Have a great day",
    "Have a nice weekend",
    "Good night",
    "I gotta go",
)

# Compiling regex
GREETINGS_REGEX = (
    re.compile("good (morning|afternoon|evening)", re.IGNORECASE),
    re.compile(r"\b(what's up|sup)\b(\?|)", re.IGNORECASE),
    re.compile(r"\b(hi|hello|hey|howdy)\b", re.IGNORECASE),
)

SPECIAL_GREETINGS_REGEX = (
    re.compile(
        "(it('s| is| was) |)(a |)(nice|great|pleased|pleasure) to meet (you|u)(.|)",
        re.IGNORECASE,
    ),
    re.compile("how( are|'re|) (you|u) doin(g|'|)\?", re.IGNORECASE),
    re.compile("how( is|'s|) it going( on|)\?", re.IGNORECASE),
    re.compile("how( have|'ve|) you been\?", re.IGNORECASE),
)

FAREWELLS_REGEX = (
    re.compile("(good night|goodbye|goodnight)", re.IGNORECASE),
    re.compile("see (you|u|ya)( soon| later| tomorrow|)", re.IGNORECASE),
    re.compile("have a (great|nice|good) (day|night|week|weekend)", re.IGNORECASE),
    re.compile("best regards", re.IGNORECASE),
    re.compile(
        r"\b(by+e+)+\b", re.IGNORECASE
    ),  # it matches 'bye', 'bye bye', 'byyyyyyye', 'byeeeee', etc.
)


def greetings_and_farewells(text, seed=0, max_output=1):
    random.seed(seed)

    output_texts = []

    for _ in itertools.repeat(None, max_output):
        processed_text = text

        for regex_tuple, replaceable_choices in zip(
            [GREETINGS_REGEX, SPECIAL_GREETINGS_REGEX, FAREWELLS_REGEX],
            [GREETINGS, SPECIAL_GREETINGS, FAREWELLS],
        ):
            for regex in regex_tuple:
                processed_text = regex.sub(
                    random.choice(replaceable_choices), processed_text
                )

        output_texts.append(processed_text)

    return output_texts


class GreetingsAndFarewells(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]

    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__()
        self.seed = seed
        self.max_output = max_output

    def generate(self, sentence: str):
        processed_text = greetings_and_farewells(
            text=sentence, seed=self.seed, max_output=self.max_output
        )
        return processed_text
