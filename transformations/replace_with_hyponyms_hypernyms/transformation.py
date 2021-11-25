import numpy as np
import spacy
import random
from checklist.editor import Editor

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ReplaceHyponyms(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "tokenizer-required",
        "meaning-alteration",
        "high-precision",
        "high-generations",
    ]

    def __init__(self, n=1, seed=0, max_output=2):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n
        self.max_output = max_output
        self.editor = Editor()

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        words = []
        perturbed_texts = []
        tokens = self.nlp(sentence)
        #Shuffle the tokens list so that all noun (and not just the beginning nouns) 
        #have a fair chance at being picked.
        shuf_tokens = list(tokens)
        random.seed(0) #To get the same output as in test.json
        random.shuffle(shuf_tokens)
        for token in shuf_tokens:
            if token.pos_ == 'NOUN':
              words.append(token)
              hyp_list = self.editor.hyponyms(sentence, token.text)
              for hyp in hyp_list:
                #Replace the noun with the hyponym
                perturbed_texts.append(sentence.replace(token.text,hyp))
              if len(perturbed_texts)>=self.max_output:
                break
        perturbed_texts = (
            perturbed_texts[: self.max_output]
            if len(perturbed_texts) > 0
            else [sentence]
        )
        return perturbed_texts

class ReplaceHypernyms(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "tokenizer-required",
        "meaning-alteration",
        "high-precision",
        "high-generations",
    ]

    def __init__(self, n=1, seed=0, max_output=2):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n
        self.max_output = max_output
        self.editor = Editor()

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        words = []
        perturbed_texts = []
        tokens = self.nlp(sentence)
        #Shuffle the tokens list so that all noun (and not just the beginning nouns) 
        #have a fair chance at being picked.
        shuf_tokens = list(tokens)
        random.seed(0) #To get the same output as in test.json
        random.shuffle(shuf_tokens)
        for token in shuf_tokens:
            if token.pos_ == 'NOUN':
              words.append(token)
              hyp_list = self.editor.hypernyms(sentence, token.text)
              for hyp in hyp_list:
                #Replace the noun with the hypernym
                perturbed_texts.append(sentence.replace(token.text,hyp))
              if len(perturbed_texts)>=self.max_output:
                break
        perturbed_texts = (
            perturbed_texts[: self.max_output]
            if len(perturbed_texts) > 0
            else [sentence]
        )
        return perturbed_texts

#Uncomment the following to get the test.json output
'''
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    transformation = ReplaceHyponyms(max_output=13)
    sentences = ["Andrew finally returned the French book to Chris that I bought last week.",
                  "This car looks fascinating","There is no love for this product.",
                  "United Airlines has horrible service"]
    test_cases = []
    for sentence in sentences:
        test_cases.append({
            "class": transformation.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in transformation.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(transformation.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=4))
    transformation = ReplaceHypernyms(max_output=13)
    sentences = ["Andrew finally returned the French book to Chris that I bought last week.",
                  "This car looks fascinating","There is no love for this product.",
                  "United Airlines has horrible service"]
    test_cases = []
    for sentence in sentences:
        test_cases.append({
            "class": transformation.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in transformation.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(transformation.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=4))
'''
