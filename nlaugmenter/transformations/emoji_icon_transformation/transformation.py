import json
import os
import random
from typing import List

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


# Check if any emoji(icon) from dict1 in text and substitute them with a random corresponding icon(emoji) from dict2
def convert(perturbed_text: str, dict1: dict, dict2: dict) -> str:
    for k in dict1:  # k is the emoji/icon type (e.g., ":)" is of type smiley
        for s in dict1[k]:
            if s in perturbed_text:
                perturbed_text = perturbed_text.replace(
                    s, random.choice(dict2[k])
                )
    return perturbed_text


# generate max_outputs different perturbed texts for each text, selecting if translating emoji to icon or icon to emoji with emoji_to_icon variable
def emoji2icon(
    text: str,
    text2emoji: dict,
    text2icon: dict,
    seed: int = 42,
    max_outputs: int = 1,
    emoji_to_icon: bool = True,
) -> List[str]:
    random.seed(seed)

    perturbed_texts = []
    for _ in range(max_outputs):
        perturbed_text = text
        if emoji_to_icon:
            perturbed_text = convert(perturbed_text, text2emoji, text2icon)
        else:
            perturbed_text = convert(perturbed_text, text2icon, text2emoji)
        perturbed_texts.append(perturbed_text)
    return perturbed_texts


class EmojiToIcon(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["All"]
    keywords = ["rule-based", "visual", "high-precision", "low-coverage"]

    def __init__(
        self, seed: int = 42, max_outputs: int = 1, emoji_to_icon: bool = False
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.emoji_to_icon = emoji_to_icon

        text2emoji_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "text2emoji.json"
        )

        text2icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "text2icon.json"
        )

        self.text2emoji = json.load(open(text2emoji_path, "r"))
        self.text2icon = json.load(open(text2icon_path, "r"))

    def generate(self, sentence: str) -> List[str]:
        perturbed_texts = emoji2icon(
            text=sentence,
            text2emoji=self.text2emoji,
            text2icon=self.text2icon,
            seed=self.seed,
            max_outputs=self.max_outputs,
            emoji_to_icon=self.emoji_to_icon,
        )
        return perturbed_texts
