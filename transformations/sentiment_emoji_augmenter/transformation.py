import numpy as np

from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType

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
    ("grin", +1.00): [">:D", ":-D", ":D", "=-D", "=D", "X-D", "x-D", "XD", "xD", "8-D"],
    ("taunt", +0.75): [">:P", ":-P", ":P", ":-p", ":p", ":-b", ":b", ":c)", ":o)", ":^)"],
    ("smile", +0.50): [">:)", ":-)", ":)", "=)", "=]", ":]", ":}", ":>", ":3", "8)", "8-)"],
    ("wink", +0.25): [">;]", ";-)", ";)", ";-]", ";]", ";D", ";^)", "*-)", "*)"],
    ("blank", +0.00): [":-|", ":|"],
    ("gasp", -0.05): [">:o", ":-O", ":O", ":o", ":-o", "o_O", "o.O", "°O°", "°o°"],
    ("worry", -0.25): [">:/", ":-/", ":/", ":\\", ">:\\", ":-.", ":-s", ":s", ":S", ":-S", ">.>"],
    ("frown", -0.75): [">:[", ":-(", ":(", "=(", ":-[", ":[", ":{", ":-<", ":c", ":-c", "=/"],
    ("cry", -1.00): [":'(", ":'''(", ";'("]
}

positive_emojis = lambda threshold: [k for k in emoji.keys() if k[1] > threshold]
neutral_emojis = lambda threshold: [k for k in emoji.keys() if 0.2 > k[1] > -threshold]
negative_emojis = lambda threshold: [k for k in emoji.keys() if k[1] < - threshold]


class SentimentEmojiAugmenter(SentenceAndTargetOperation):
    """Adds a positive labelled emoji as well as a positive emoteicon for positive sentences and vice versa.
    And neutral smiley for unlabelled and neutral sentences.
    Check line number 12 and 25 to decide a good threshold.
    """
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = "All"
    tgt_languages = "All"

    def __init__(self, seed=0, threshold=0.2):
        super().__init__(seed)
        self.seed = seed
        np.random.seed(self.seed)
        self.threshold = threshold

    def generate(self, sentence: str, target: str):
        if target is None:
            emotions = self.get_emotions("neutral", self.threshold)
        elif str(target) in ["1", "pos", "positive"]:
            emotions = self.get_emotions("pos", self.threshold)
        elif str(target) in ["0", "neg", "negative"]:
            emotions = self.get_emotions("neg", self.threshold)
        else:
            emotions = self.get_emotions("neutral", self.threshold)
        perturbed_sentences = [sentence + " " + emotion for emotion in emotions if emotion.strip()]
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
        if sentiment is "pos":
            pe = positive_emojis(threshold)
            keys = np.random.randint(0, len(pe) - 1, k1)
        elif sentiment is "neg":
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



# Sample code to demonstrate adding test cases.


# Sample code to demonstrate adding test cases.
'''
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = SentimentEmojiAugmenter()
    test_cases = []
    src = ["Andrew is a happy guy!",
           "Alex is unhappy"
           " because he keeps cribbing about his work."]
    tgt = ["1",
           "-1", ]
    for idx, (sentence, target) in enumerate(zip(src, tgt)):
        perturbeds = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": []}
        )
        for sentence, target in perturbeds:
            test_cases[idx]["outputs"].append({"sentence": sentence, "target": target})
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
'''