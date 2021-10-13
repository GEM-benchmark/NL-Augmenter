import random
import json
import spacy
import os.path

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def abbreviate(self, text, nlp, prob = 0.25, seed = 0, max_outputs = 1):
    random.seed(seed)
    transf = []
    for _ in range(max_outputs):
        trans_text = text
        for phrase in self.phrase_abbrev_dict:
            if random.random() < prob:
                trans_text = trans_text.replace(phrase, self.phrase_abbrev_dict[phrase])
        doc = nlp(trans_text).doc
        trans = []
        for token in doc:
            word = token.text
            if word in self.word_abbrev_dict and random.random() < prob:
                trans.append(self.word_abbrev_dict[word])
            else:
                trans.append(word)
        trans1 = " ".join([str(word) for word in trans])
        transf.append(trans1)
        res = tuple(transf)
    return res


class Abbreviate(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION,
            TaskType.TEXT_CLASSIFICATION]
    languages = ["en"]
    keywords = ["lexical", "external-knowledge-based", "highly-meaning-preserving"]

    def __init__(self, prob = 0.5, seed = 0, max_outputs = 1):
        #reading in slang dictionaries
        scriptpath = os.path.dirname(__file__)
        with open(os.path.join(scriptpath, 'phrase_abbrev_dict.json'),'r') as file:
            self.phrase_abbrev_dict = json.loads(file.read())
        with open(os.path.join(scriptpath, 'word_abbrev_dict.json'), 'r') as file:
            self.word_abbrev_dict = json.loads(file.read())

        super().__init__(seed)
        self.prob = prob
        self.max_outputs = max_outputs
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):
        perturbed = abbreviate(self,
            text = sentence, nlp = self.nlp, prob = self.prob, seed = self.seed, max_outputs = self.max_outputs
        )
        return perturbed
    
"""if __name__ == '__main__':
    import json
    
    tf = Abbreviate()
    sentence = "I will turn in the homework on Friday for sure!"
    test_cases = []
    
    for sentence in  ["I will turn in the homework on Friday for sure!",
           "I love you bro, but for the love of god, just google it.",
           "Just so you know, we have a meeting in two hours.",
           "You driving at 80 miles per hour is why insurance is so freaking expensive.",
           "My bad, my bad, this is my first time playing a First Person Shooter."]:
    
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence},
            "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
       
    with open('test.json', 'w') as f:
        content = {"type": "abbreviate", "test_cases": test_cases}
        json.dump(content, f)"""
