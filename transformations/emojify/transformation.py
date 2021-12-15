import os
import random
from json import load

import spacy

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def emojify(sentence, nlp, word_to_emoji, prob=1, seed=0, max_outputs=1):

    random.seed(seed)
    doc = nlp(sentence)
    results = []

    for _ in range(max_outputs):

        # Reconstruct the sentence with replaced lemma
        transformed_sentence = ""

        for token in doc:
            lemma = token.lemma_.lower()

            # Handle numeric tokens
            if lemma.isnumeric():
                if random.random() < prob:
                    for digit in list(lemma):
                        emoji = digit
                        if digit in word_to_emoji:
                            emoji = random.choice(word_to_emoji[digit])
                        transformed_sentence += emoji

                    if " " in token.text_with_ws:
                        transformed_sentence += " "

                else:
                    transformed_sentence += token.text_with_ws

            elif lemma in word_to_emoji:
                # We have `prob` chance to replace this token with emoji
                if random.random() < prob:

                    # Randomly choose a emoji candidate for this token
                    emoji = random.choice(word_to_emoji[lemma])
                    transformed_sentence += emoji

                    if " " in token.text_with_ws:
                        transformed_sentence += " "

                else:
                    transformed_sentence += token.text_with_ws

            else:
                # If lemma is not in the emoji dictionary, we keep it the same
                transformed_sentence += token.text_with_ws

        results.append(transformed_sentence)

    return results


class EmojifyTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=2022, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

        # Load the emoji dictionary
        dict_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "emoji_dict.json"
        )
        self.word_to_emoji = load(open(dict_path, "r"))

        # Load the spacy nlp
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        """
        Emojify the sentence.
        """

        perturbed_texts = emojify(
            sentence,
            self.nlp,
            self.word_to_emoji,
            prob=1,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts
