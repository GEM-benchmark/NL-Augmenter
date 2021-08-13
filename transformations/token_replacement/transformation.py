import random
import spacy

from typing import List

from initialize import spacy_nlp

from interfaces.SentenceOperation import SentenceOperation

from tasks.TaskTypes import TaskType

from transformations.token_replacement.lookup_table_utils import (
    load_lookup, 
    get_token_replacement,
)


"""
Implementation of the token replacement perturbation using lookup tables 
with valid replacement candidates
"""
  
class TokenReplacement(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(
        self, seed=0, max_outputs = 1, replacement_prob = 1.0, min_length = 3, 
        max_dist = 1, lookup = ["typos.xz", "ocr.xz"]):
        """
        :param seed: random seed
        :param max_outputs: max. number of outputs to generate
        :param replacement_prob: replacement probability [0.0, 1.0]
        :param min_length: min. length of token that can be perturbed
        :param max_dist: max. Levenshtein distance between the original and the
                         perturbed token
        :param lookup: dictionary or a list of files with lookup tables
        """
        super().__init__(seed, max_outputs=max_outputs)
        
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.replacement_prob = replacement_prob
        self.max_dist = max_dist
        self.min_length = min_length
        
        if isinstance(lookup, dict):
            self.lookup = lookup
        else:
            self.lookup = load_lookup(lookup)

    def generate(self, sentence: str) -> List[str]:

        random.seed(self.seed)        
        
        perturbed_sentences = []
        
        for _ in range(self.max_outputs):
            
            perturbed_tokens = []
            for tok in self.nlp(sentence):
            
                text = tok.text
                if text in self.lookup and random.random() <= self.replacement_prob:
                    text = get_token_replacement(text, self.lookup,
                        self.min_length, self.max_dist)
       
                if tok.whitespace_:
                    text += " "
       
                perturbed_tokens.append(text)
            
            perturbed_sentences.append(''.join(token for token in perturbed_tokens))

        return perturbed_sentences


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.

if __name__ == '__main__':

    import json, os
    from TestRunner import convert_to_snake_case

    tf = TokenReplacement(max_outputs=1)
    test_cases = []
    src = ["Manmohan Singh served as the PM of India.",
           "Neil Alden Armstrong was an American astronaut.",
           "Katheryn Elizabeth Hudson is an American singer.",
           "The owner of the mall is Anthony Gonsalves.",
           "Roger Michael Humphrey Binny (born 19 July 1955) is an Indian " +
           "former cricketer."]

    for idx, sent in enumerate(src):
        outputs = tf.generate(sent)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sent},
            "outputs": []}
        )
        for out in outputs:
            test_cases[idx]["outputs"].append({"sentence": out})

    json_file = {"type": convert_to_snake_case(tf.name()), 
        "test_cases": test_cases}
    #print(json.dumps(json_file))
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, "test.json"), "w") as f:
        json.dump(json_file, f, indent=2, ensure_ascii=False)

"""
