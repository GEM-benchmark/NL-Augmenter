#import itertools
import random
import numpy as np
import re
import copy
import random
from typing import List

from transformers import BertTokenizer, BertForMaskedLM
from sentence_transformers import SentenceTransformer, util

from torch.nn import functional as F
import torch

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def _mask_word(sentence, word_to_mask, tokenizer):
    """ helper function,
    replace word in a sentence with mask-token, as prep for BERT tokenizer"""
    start_index = sentence.find(word_to_mask)
    return sentence[0:start_index] + tokenizer.mask_token + sentence[
        start_index + len(word_to_mask):]


def get_k_replacement_words(tokenized_text, tokenizer, model, k):
    """return k most similar words from the model, for a tokenized mask-word in a sentence.

    Args:
        tokenized_text (str): sentence with a word masked out
        model ([type]): model
        tokenizer ([type]): tokenizer
        k (int, optional): how many similar words to find for a given tokenized-word. Defaults to 5.

    Returns:
        [list]: list of top k words
    """
    inputs = tokenizer.encode_plus(tokenized_text, return_tensors='pt')
    index_to_mask = torch.where(inputs.input_ids[0] == tokenizer.mask_token_id)
    outputs = model(**inputs)
    softmax = F.softmax(outputs.logits, dim=-1)
    mask_word = softmax[0, index_to_mask, :]

    #return torch.topk(mask_word, k)[1][0]

    sorted_tokens = torch.argsort(mask_word[0], descending=True)
    i = 0
    valid_tokens = []
    while len(valid_tokens) < k and i < len(sorted_tokens):
        if tokenizer.decode([sorted_tokens[i]]).isalnum():
            valid_tokens.append(sorted_tokens[i])
        i += 1
    assert len(valid_tokens) == k or i == len(sorted_tokens)    # We either have found k valid (non punctuation) tokens or we have looked through all the tokens.
    return valid_tokens

def single_sentence_random_step(sentence, tokenizer, model, k):
    """For a given sentence, choose a random word to mask, and
    replace it with a word the top-k most similar words in BERT model.
    Return k sentences, each with a different replacement word for the mask.

    Args:
        sentence ([type]): sentence to perform random walk on
        tokenizer ([type]): tokenizer
        model ([type]): model
        k (int, optional): how many replacement words to try. Defaults to 5.

    Returns:
        [list]: k-sentences with masked word replaced with top-k most similar words
    """
    text_split = re.split('[ ?.,!;"]', sentence)

    # pick a random word to mask
    word_to_mask = random.choice(text_split)
    while len(word_to_mask) == 0 and not word_to_mask.isalnum(): # Avoid empty strings in split text
        word_to_mask = random.choice(text_split)
    # mask word
    new_text = _mask_word(sentence, word_to_mask, tokenizer)

    # get k replacement words
    top_k = get_k_replacement_words(new_text, tokenizer, model, k=k)

    # replace mask-token with the word from the top-k replacements
    return [
        new_text.replace(tokenizer.mask_token, tokenizer.decode([token]))
        for token in top_k if tokenizer.decode([token]).isalnum()
    ]


def single_round(sentences: List[str], tokenizer, model, k) -> List[str]:
    """For a given list of sentences, do a random walk on each sentence.

    Args:
        sentences ([type]): list of sentnces to perform random walk on
        tokenizer ([type]): tokenizer
        model ([type]): model

    Returns:
        [List]: list of random-walked sentences
    """
    new_sentences = []

    for sentence in sentences:
        new_sentences.extend(
            single_sentence_random_step(sentence, tokenizer, model, k))

    return new_sentences


def random_walk(original_text: str, steps: int, k: int, tokenizer,
                model) -> List[str]:
    old_sentences = [original_text]

    # Do k steps of random walk procedure
    for _ in range(steps):
        sentences = single_round(old_sentences, tokenizer, model, k)
        old_sentences = copy.deepcopy(sentences)

    #assert len(sentences) == k**steps  # This may not be possible if we cannot find k non-punctuation suggestions.
    return sentences

def sentence_similarity_metric(similarity_model, sen_A, sen_B):
    emb_A = similarity_model.encode(sen_A)
    emb_B = similarity_model.encode(sen_B)

    score = util.pytorch_cos_sim(emb_A, emb_B)
    return score

class RandomWalk(SentenceOperation):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    # Default parameters match those of the 'test.json' below.
    def __init__(self, seed=0, max_outputs=3, steps=5, k=2, sim_req=0.25):
        random.seed(seed)
        np.random.seed(seed)
        super().__init__(seed, max_outputs=max_outputs)
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
        self.model = BertForMaskedLM.from_pretrained('bert-large-cased')
        self.sim_model = SentenceTransformer('all-mpnet-base-v2')
        self.max_outputs = max_outputs
        self.steps = steps
        self.k = k
        self.sim_req = sim_req

    def generate(self, sentence: str):
        print('Random walking on the sentence:', sentence)
        perturbed_texts = random_walk(
            original_text=sentence,
            steps=self.steps,
            k=self.k,
            tokenizer=self.tokenizer,
            model=self.model
        )

        scores = []
        for o in perturbed_texts:
            scores.append(sentence_similarity_metric(self.sim_model, sentence, o))
        valid_sentences = np.array(scores) > self.sim_req
        perturbed_texts = [o for o,s in zip(perturbed_texts, valid_sentences) if s]
        assert np.sum(valid_sentences) == len(perturbed_texts)

        if len(perturbed_texts) > self.max_outputs:
            perturbed_texts = random.sample(perturbed_texts, self.max_outputs)
        return perturbed_texts

"""
# The code to produce 'test.json' must be commented out so that pytest succeeds.
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = RandomWalk(max_outputs=3, k=2, steps=5, sim_req=0.25)
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
"""