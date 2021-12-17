import numpy as np

from nlaugmenter.interfaces.SentenceOperation import SentenceAndTargetOperation
from nlaugmenter.tasks.TaskTypes import TaskType

"""
Adds a positive labelled emoji as well as a positive emoteicon for positive sentences and vice versa.
And neutral smiley for unlabelled and neutral sentences.
Since IMDB has labels +1 --> str(target) in ["1", "pos", "positive"] is used to determine if it's positive.
"""

emoji = {  # (facial expression, sentiment)-keys
    ("love", +1.00): ["❤️"],
    ("grin", +1.00): ["😀", "😄", "😃", "😆", "😅", "😂", "😁", "😻", "😍", "😈"],
    ("taunt", +0.75): ["😛", "😝", "😜", "😋", "😇"],
    ("smile", +0.50): ["😊", "😌", "😏", "😎", "☺"],
    ("wink", +0.25): ["😉"],
    ("blank", +0.00): ["😐", "😶"],
    ("gasp", -0.05): ["😳", "😮", "😯", "😧", "😦", "🙀"],
    ("worry", -0.25): ["😕", "😬"],
    ("frown", -0.75): ["😟", "😒", "😔", "😞", "😠", "😩", "😫", "😡"],
    ("cry", -1.00): ["😢", "😥", "😓", "😪", "😭", "😿"],
}

emoticons = {  # (facial expression, sentiment)-keys
    ("love", +1.00): ["<3", "♥", "❤"],
    ("grin", +1.00): [
        ">:D",
        ":-D",
        ":D",
        "=-D",
        "=D",
        "X-D",
        "x-D",
        "XD",
        "xD",
        "8-D",
    ],
    ("taunt", +0.75): [
        ">:P",
        ":-P",
        ":P",
        ":-p",
        ":p",
        ":-b",
        ":b",
        ":c)",
        ":o)",
        ":^)",
    ],
    ("smile", +0.50): [
        ">:)",
        ":-)",
        ":)",
        "=)",
        "=]",
        ":]",
        ":}",
        ":>",
        ":3",
        "8)",
        "8-)",
    ],
    ("wink", +0.25): [
        ">;]",
        ";-)",
        ";)",
        ";-]",
        ";]",
        ";D",
        ";^)",
        "*-)",
        "*)",
    ],
    ("blank", +0.00): [":-|", ":|"],
    ("gasp", -0.05): [
        ">:o",
        ":-O",
        ":O",
        ":o",
        ":-o",
        "o_O",
        "o.O",
        "°O°",
        "°o°",
    ],
    ("worry", -0.25): [
        ">:/",
        ":-/",
        ":/",
        ":\\",
        ">:\\",
        ":-.",
        ":-s",
        ":s",
        ":S",
        ":-S",
        ">.>",
    ],
    ("frown", -0.75): [
        ">:[",
        ":-(",
        ":(",
        "=(",
        ":-[",
        ":[",
        ":{",
        ":-<",
        ":c",
        ":-c",
        "=/",
    ],
    ("cry", -1.00): [":'(", ":'''(", ";'("],
}


def positive_emojis(threshold):
    return [k for k in emoji.keys() if k[1] > threshold]


def neutral_emojis(threshold):
    return [k for k in emoji.keys() if 0.2 > k[1] > -threshold]


def negative_emojis(threshold):
    return [k for k in emoji.keys() if k[1] < -threshold]


def find_all_char_positions(text, c):
    idx = text.find(c)
    while idx != -1:
        yield idx
        idx = text.find(c, idx + 1)


class SentimentEmojiAugmenter(SentenceAndTargetOperation):
    """Adds a positive labelled emoji as well as a positive emoteicon for positive sentences and vice versa.
    And neutral smiley for unlabelled and neutral sentences.
    Check line number 12 and 25 to decide a good threshold.
    Link to code: This split comes from the library https://github.com/clips/pattern which was used as a source for these. And I think theoretically emojis are images while emoticons are keyboard characters.
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = "All"
    tgt_languages = "All"

    def __init__(self, seed=0, threshold=0.2, exaggeration=2, k=2):
        super().__init__(seed)
        self.seed = seed
        np.random.seed(self.seed)
        self.threshold = threshold
        self.exaggeration = exaggeration
        self.k = k

    def generate(self, sentence: str, target: str):
        if target is None:
            emotions = self.get_emotions("neutral", self.threshold)
        elif str(target) in ["1", "pos", "positive"]:
            emotions = self.get_emotions("pos", self.threshold)
        elif str(target) in ["0", "neg", "negative"]:
            emotions = self.get_emotions("neg", self.threshold)
        else:
            emotions = self.get_emotions("neutral", self.threshold)

        spaces = find_all_char_positions(sentence, " ")
        a = [s for s in spaces]
        perturbed_sentences = []
        if len(a) > self.k > 0:
            i_s = np.random.choice(a, self.k)
            for i in i_s:
                perturbed_sentences.append(
                    [
                        sentence[:i]
                        + (emotion * self.exaggeration)
                        + sentence[i:]
                        for emotion in emotions
                        if emotion.strip()
                    ]
                )

        perturbed_sentences.extend(
            [
                sentence + " " + (emotion * self.exaggeration)
                for emotion in emotions
                if emotion.strip()
            ]
        )
        perturbed_sentences.extend(
            [
                (emotion * self.exaggeration) + " " + sentence
                for emotion in emotions
                if emotion.strip()
            ]
        )

        perturbed_target = target

        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_sentences}\nLabel: {perturbed_target}"
            )
        perturbations = []
        for p in perturbed_sentences:
            perturbations.append((p, perturbed_target))
        return perturbations

    def get_emotions(self, sentiment, threshold, k1=2):
        additions = []
        if sentiment == "pos":
            pe = positive_emojis(threshold)
            keys = np.random.randint(0, len(pe) - 1, k1)
        elif sentiment == "neg":
            ne = negative_emojis(threshold)
            keys = np.random.randint(0, len(ne) - 1, k1)
        else:
            ne = neutral_emojis(threshold)
            keys = np.random.randint(0, len(ne) - 1, k1)
        for index in keys:
            # random.seed(self.seed)
            key = list(emoji)[index]
            additions.extend(np.random.choice(emoji.get(key)))
            # random.seed(self.seed)
            key = list(emoticons)[index]
            additions.extend(np.random.choice(emoticons.get(key)))
        return additions
