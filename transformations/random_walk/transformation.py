import itertools
import random
from transformers import BertTokenizer, BertForMaskedLM
from torch.nn import functional as F
import torch
import numpy as np
import re
import copy
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""

def random_walk(original_text, steps, k, tokenizer, model):
    sentences = []
    old_sentences = [original_text]
    for i in range(steps): # Do k steps of random walk procedure
        sentences = []
        for text in old_sentences:
            text_split = re.split('[ ?.,!;"]', text)
            splits = len(text_split)
            index_to_mask = np.random.randint(splits)
            while len(text_split[index_to_mask]) == 0:
                index_to_mask = np.random.randint(splits)
            word_to_mask = text_split[index_to_mask]
            # print('Word to mask:', word_to_mask)
            start_index = text.find(word_to_mask)
            new_text = text[0:start_index] + tokenizer.mask_token + text[start_index + len(word_to_mask):]

            inputs = tokenizer.encode_plus(new_text, return_tensors='pt')
            index_to_mask = torch.where(inputs.input_ids[0] == tokenizer.mask_token_id)
            outputs = model(**inputs)
            logits = outputs.logits
            softmax = F.softmax(logits, dim=-1)
            mask_word = softmax[0, index_to_mask, :]
            top_k = torch.topk(mask_word, k)[1][0]

            for token in top_k:
                word = tokenizer.decode([token])
                new_sentence = new_text.replace(tokenizer.mask_token, word)
                sentences.append(new_sentence)

        old_sentences = copy.deepcopy(sentences)
    assert len(sentences) == k**steps
    return sentences




class RandomWalk(SentenceOperation):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1, steps=5, k=2):
        super().__init__(seed, max_outputs=max_outputs)
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
        self.model = BertForMaskedLM.from_pretrained('bert-large-cased')
        self.max_outputs = max_outputs
        self.steps = steps
        self.k = k

    def generate(self, sentence: str):
        perturbed_texts = random_walk(
            original_text=sentence,
            steps=self.steps,
            k=self.k,
            tokenizer=self.tokenizer,
            model=self.model
        )
        if len(perturbed_texts) > self.max_outputs:
            perturbed_texts = random.sample(perturbed_texts, self.max_outputs)
        return perturbed_texts


# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = RandomWalk(max_outputs=3, k=2, steps=5)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))

    with open('test.json', 'w') as f:
        json.dump(json_file, f, indent=2)
