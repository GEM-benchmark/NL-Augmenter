import json
import os
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def convert(perturbed_text, dict1, dict2):
    for k in dict1:
        for s in dict1[k]:
            if s in perturbed_text:
                perturbed_text = perturbed_text.replace(
                    s, random.choice(dict2[k])
                )
    return perturbed_text


def emoji2icon(
    text, text2emoji, text2icon, seed=42, max_outputs=1, emoji_to_icon=True
):
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

    def __init__(self, seed=42, max_outputs=1, emoji_to_icon=False):
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

    def generate(self, sentence: str):
        perturbed_texts = emoji2icon(
            text=sentence,
            text2emoji=self.text2emoji,
            text2icon=self.text2icon,
            seed=self.seed,
            max_outputs=self.max_outputs,
            emoji_to_icon=self.emoji_to_icon,
        )
        return perturbed_texts
