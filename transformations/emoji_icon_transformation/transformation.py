import itertools
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


def emoji2icon(text, seed=42, max_outputs=1, emoji_to_icon=True):
    random.seed(seed)

    icons = {
        "smiley": [
            ":‑)",
            ":)",
            ":-]",
            ":]",
            ":-3",
            ":3",
            ":->",
            ":>",
            "8-)",
            "8)",
            ":-}",
            ":}",
            ":o)",
            ":c)",
            ":^)",
            "=]",
            "=)",
        ],
        "laughing": [
            ":‑D",
            ":D",
            "8‑D",
            "8D",
            "x‑D",
            "xD",
            "X‑D",
            "XD",
            "=D",
            "=3",
            "B^D",
            "c:",
            "C:",
        ],
        "sad": [
            ":‑(",
            ":(",
            ":‑c",
            ":c",
            ":‑<",
            ":<",
            ":‑[",
            ":[",
            ":(",
            ";(",
        ],
        "angry": [">:[", ":{", ":@"],
        "crying": [":'‑(", ":'("],
        "tears_of_happiness": [":'‑)", ":')"],
        "disgust": ["D‑':", "D:<", "D:", "D8", "D;", "D=", "DX"],
        "surprise": [":‑O", ":O", ":‑o", ":o", ":-0", "8‑0", ">:O"],
        "kiss": [":-*", ":*", ":×"],
        "wink": [
            ";‑)",
            ";)",
            "*-)",
            "*)",
            ";‑]",
            ";]",
            ";^)",
            ";>",
            ":‑,",
            ";D",
        ],
        "tongue": [
            ":‑P",
            ":P",
            "X‑P",
            "XP",
            "x‑p",
            "xp",
            ":‑p",
            ":p",
            ":‑Þ",
            ":Þ",
            ":‑þ",
            ":þ",
            ":‑b",
            ":b",
            "d:",
            "=p",
            ">:P",
        ],
        "skeptical": [
            ":-/",
            ":/",
            ":‑.",
            ">:\\",
            ">:/",
            ":\\",
            "=/",
            "=\\",
            ":L",
            "=L",
            ":S",
        ],
        "straight_face": [":‑|", ":|"],
        "embarassed": [":$", "://)", "://3"],
        "sealed_lips": [":‑X", ":X", ":‑#", ":#", ":‑&", ":&"],
        "angel": ["O:‑)", "O:)", "0:‑3", "0:3", "0:‑)", "0:)", "0;^)"],
        "evil": [
            ">:‑)",
            ":)",
            "}:‑)",
            "}:)",
            "3:‑)",
            "3:)",
            ">;)",
            ">:3",
            ";3",
        ],
        "cool": ["|;‑)", "B-)"],
        "bored": ["|‑O"],
        "tongue_in_cheek": [":‑J"],
        "confused": ["%‑)", "%)"],
        "sick": [":‑###..", ":###.."],
        "disbelief": ["',:-|", "',:-l"],
        "awkward": [":E"],
        "skull": ["8-X", "8=X", "x-3", "x=3"],
    }

    emojis = {
        "smiley": ["☺️", "🙂", "😊", "😀", "😁"],
        "laughing": ["😃", "😄", "😆", "😍"],
        "sad": ["☹️", "🙁", "😞", "😟", "😣"],
        "angry": ["😠", "😡", "😖"],
        "crying": ["😢", "😭"],
        "tears_of_happiness": ["🥲", "😂"],
        "disgust": ["😨", "😧", "😦", "😱", "😫", "😩"],
        "surprise": ["😮", "😯", "😲"],
        "kiss": ["😗", "😙", "😚", "😘"],
        "wink": ["😉", "😜"],
        "tongue": ["😛", "😝", "😜", "🤑"],
        "skeptical": ["🤔", "😕", "😟"],
        "straight_face": ["😐", "😑"],
        "embarassed": ["😳", "😞", "😖"],
        "sealed_lips": ["🤐", "😶"],
        "angel": ["😇", "👼"],
        "evil": ["😈"],
        "cool": ["😎"],
        "bored": ["😪"],
        "tongue_in_cheek": ["😏", "😒"],
        "confused": ["😵", "😕", "🤕", "😵‍💫"],
        "sick": ["🤒", "😷", "🤢"],
        "disbelief": ["🤨"],
        "awkward": ["😬"],
        "skull": ["☠️", "💀", "🏴‍☠️"],
    }

    perturbed_texts = []
    for _ in itertools.repeat(None, max_outputs):
        perturbed_text = text
        if emoji_to_icon:
            perturbed_text = convert(perturbed_text, emojis, icons)
        else:
            perturbed_text = convert(perturbed_text, icons, emojis)
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

    def generate(self, sentence: str):
        perturbed_texts = emoji2icon(
            text=sentence,
            seed=self.seed,
            max_outputs=self.max_outputs,
            emoji_to_icon=self.emoji_to_icon,
        )
        return perturbed_texts
