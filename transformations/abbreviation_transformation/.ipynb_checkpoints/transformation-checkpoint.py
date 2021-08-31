import random
import json
import spacy

from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType

with open('phrase_abbrev_dict.json','r') as file:
    phrase_abbrev_dict = json.loads(file.read())
with open('word_abbrev_dict.json', 'r') as file:
    word_abbrev_dict = json.loads(file.read())
    

def abbreviate(text, prob = 0.5, seed = 0, max_outputs = 1):
    random.seed(seed)
    transf = []
    for _ in range(max_outputs):
        trans_text = text
        for phrase in phrase_abbrev_dict:
            if phrase in trans_text:
                trans_text.replace(phrase, phrase_abbrev_dict[phrase])
        doc = nlp(trans_text)
        trans = []
        for token in doc:
            random_num = random.random()
            word = token.text
            if word in word_abbrev_dict and random_num < prob:
                trans.append(word_abbrev_dict[word])
            else:
                trans.append(word)
        transf.append(trans)
    return transf


class Abbreviate(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    tgt_languages = ["en"]

    def __init__(self, prob = 0.5, seed = 0, max_outputs = 1):
        super().__init__(seed)
        self.prob = prob
        self.max_outputs = max_outputs

    def generate(self, sentence: str, target: str):
        perturbed = abbreviate(
            text = sentence, prob = self.prob, seed = self.seed, max_outputs = self.max_outputs
        )
        return perturbed
    
if __name__ == '__main__':
    import json
    
    tf = Abbreviate()
    examples = []
    
    src = ["I will turn in the homework on Friday for sure!",
           "I love you bro, but for the love of god, just google it."
           "Just so you know, we have a meeting in two hours."
           "You driving at 80 miles per hour is why insurance is so freaking expensive."
           "My bad, my bad, this is my first time playing a First Person Shooter."]
    
    for idx, (sentence) in enumerate(zip(src)):
        perturbeds = tf.generate(sentence)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence},
            "outputs": []}
        )
        for sentence in perturbeds:
            test_cases[idx]["outputs"].append({"sentence": sentence})
            
    f = {"type": "abbreviate", "test_cases": test_cases}
    json.dump(f)