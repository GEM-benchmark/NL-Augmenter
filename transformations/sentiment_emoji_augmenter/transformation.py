import random

from interfaces.SentenceOperation import SentenceAndTargetOperation
import spacy
from tasks.TaskTypes import TaskType

"""
Adds a positive labelled emoji as well as a positive emoteicon for positive sentences and vice versa. 
And neutral smiley for unlabelled and neutral sentences.
"""

emoji = {  # (facial expression, sentiment)-keys
    ("love", +1.00): ["❤️", "💜", "💚", "💙", "💛", "💕"],
    ("grin", +1.00): ["😀", "😄", "😃", "😆", "😅", "😂", "😁", "😻", "😍", "😈", "👌"],
    ("taunt", +0.75): ["😛", "😝", "😜", "😋", "😇"],
    ("smile", +0.50): ["😊", "😌", "😏", "😎", "☺", "👍"],
    ("wink", +0.25): ["😉"],
    ("blank", +0.00): ["😐", "😶"],
    ("gasp", -0.05): ["😳", "😮", "😯", "😧", "😦", "🙀"],
    ("worry", -0.25): ["😕", "😬"],
    ("frown", -0.75): ["😟", "😒", "😔", "😞", "😠", "😩", "😫", "😡", "👿"],
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

positive_emojis = [k for k in emoji.keys() if k[1] > 0.2]
neutral_emojis = [k for k in emoji.keys() if 0.2 > k[1] > -0.2]
negative_emojis = [k for k in emoji.keys() if k[1] < -0.2]


class SentimentEmojiAugmenter(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = "All"
    tgt_languages = "All"

    def __init__(self, seed=0):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.seed = seed
        random.seed(self.seed)

    def generate(self, sentence: str, target: str):
        if target is None:
            emotions = self.get_emotions("neutral")
        elif target.startswith("pos"):
            emotions = self.get_emotions("pos")
        elif target.startswith("neg"):
            emotions = self.get_emotions("neg")
        else:
            emotions = self.get_emotions("neutral")
        perturbed_sentences = [sentence + " " + emotion for emotion in emotions if emotion.strip()]
        perturbed_target = target

        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_sentences}\nLabel: {perturbed_target}"
            )
        return perturbed_sentences[0], perturbed_target

    def get_emotions(self, sentiment="pos", k1=2):
        additions = []
        random.seed(self.seed)
        if sentiment is "pos":
            keys = random.sample(positive_emojis, k1)
        elif sentiment is "neg":
            keys = random.sample(negative_emojis, k1)
        else:
            keys = random.sample(neutral_emojis, k1)
        for key in keys:
            random.seed(self.seed)
            additions.extend(random.sample(emoji.get(key), 1))
            random.seed(self.seed)
            additions.extend(random.sample(emoticons.get(key), 1))
        return additions

"""

# Sample code to demonstrate adding test cases.

if __name__ == '__main__':

    tf = SentimentEmojiAugmenter()
    test_cases = []
    src = ["The dog was happily wagging its tail.", "Ram und Sita waren glücklich verheiratet."
                                                    "Le film était bien meilleur que les 100 derniers que j'ai regardés !",
           "這部電影比我最近看的 100 部要好得多！"
           "भारत आणि कॅनडा चांगले मित्र आहेत.", "Tujuh orang terluka!",
           "அது மிக மோசமான படம், அதற்கு நான் மீண்டும் பணம் கொடுக்கவில்லை."]
    tgt = ["pos", "pos", "pos", "pos", "pos", "neg", "neg"]
    for sentence, target in zip(src, tgt):
        sentence_o, target_o = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": {"sentence": sentence_o, "target": target_o}}
        )
    json_file = {"type": tf.name(), "test_cases": test_cases}
    print(str(json_file))

"""