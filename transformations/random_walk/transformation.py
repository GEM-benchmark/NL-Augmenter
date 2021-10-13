#import itertools
import random
import numpy as np
import re
import copy
import random
from typing import List

from transformers import BertTokenizer, BertForMaskedLM
from sentence_transformers import SentenceTransformer, util
import spacy

from torch.nn import functional as F
import torch

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

def _mask_word(sentence, split_indices, mask):
    """ helper function to replace word in a sentence with mask-token, as prep 
    for BERT tokenizer
    
    Args:
    sentence (str): sentence with work to mask
    split_indices ([int, int]): index of word to replace, begining and character 
		after the end indices
    mask (BERT Token): token for a BERT mask
    
    """
    return sentence[0:split_indices[0]] + mask + sentence[
        split_indices[1]:]


def get_k_replacement_words(tokenized_text, tokenizer, model, k):
    """return k most similar words from the model, for a tokenized mask-word 
    in a sentence.

    Args:
        tokenized_text (str): sentence with a word masked out
        tokenizer ([type]): tokenizer
        model ([type]): model
        k (int): how many similar words to find for a given tokenized-word. Checks
          that generated word is a composed of letters or numbers.

    Returns:
        [list]: list of top k words
		[bool]: Whether or not we found the desired number of valid replacement words
    """
    inputs = tokenizer.encode_plus(tokenized_text, return_tensors='pt', truncation=True, max_length = 512)
    index_to_mask = torch.where(inputs.input_ids[0] == tokenizer.mask_token_id)
    if index_to_mask[0].numel() == 0: # Since we are truncating the input to be 
        # 512 tokens (BERT's max), we need to make sure the mask is in these first 512.
        # If not, return False so that we try again.
        return None, False
        # This should not occur since we split long sentences.
    outputs = model(**inputs)
    softmax = F.softmax(outputs.logits, dim=-1)
    mask_word = softmax[0, index_to_mask, :]

    sorted_tokens = torch.argsort(mask_word[0], descending=True)
    i = 0
    valid_tokens = [] # The k most probable tokens are guaranteed to be words,
    # so we make sure they are.
    while len(valid_tokens) < k and i < len(sorted_tokens):
        if tokenizer.decode([sorted_tokens[i]]).isalnum():
            valid_tokens.append(sorted_tokens[i])
        i += 1
    assert len(valid_tokens) == k or i == len(sorted_tokens)    # We either have found k valid (non punctuation) tokens or we have looked through all the tokens.
    if len(valid_tokens) < k:
        valid_tokens += (k - len(valid_tokens)) * [valid_tokens[0]]
	return valid_tokens, True


def single_sentence_random_step(sentence, tokenizer, model, nlp, names, k):
    """For a given sentence, choose a random word to mask, and
    replace it with a word the top-k most similar words in BERT model.
    Return k sentences, each with a different replacement word for the mask.

    Args:
        sentence ([type]): sentence to perform random walk on
        tokenizer ([type]): tokenizer
        model ([type]): model
        nlp ([type]): Spacy NLP model for finding named entities
        names (list): Named entities to not replace.
        k (int): how many replacement words to try.

    Returns:
        [list]: k-sentences with masked word replaced with top-k most similar words
    """
    split_iter = re.finditer(r"[\w']+|[.,!?;]", sentence) # Split sentence on puctuation.
    text_split = []
    split_indices = []
    sentence_parts = []
    text_split.append([])
    split_indices.append([])
    base_index = 0
    for m in split_iter:
        text_split[-1].append(m.group(0))
        split_indices[-1].append((m.start() - base_index, m.end() - base_index))
        
        if m.end() - base_index > 450:
            sentence_parts.append(sentence[base_index:m.end()])
            base_index = m.end()
            text_split.append([])
            split_indices.append([])
            
    sentence_parts.append(sentence[base_index:])

    # Remove any empty sentence parts.
    valid_splits = [len(ts) > 0 for ts in text_split]
    text_split = [ts for ts, vs in zip(text_split, valid_splits) if vs]
    split_indices = [si for si, vs, in zip(split_indices, valid_splits) if vs]
    sentence_parts = [sen for sen, vs in zip(sentence_parts, valid_splits) if vs]

    new_sentences = []
    for ts, si, sen in zip (text_split, split_indices, sentence_parts):		
        if len(ts) == 0:
            print(text_split, split_indices, sentence_parts)
            raise ValueError("Somehow we got a sentence part that is emtpy. Not good!")
        rand_int = np.random.randint(len(ts)) # pick a random word to mask
        word_to_mask = ts[rand_int]
        iter_count = 1
        give_up = False
        while len(word_to_mask) == 0 or not word_to_mask.isalnum() or word_to_mask in names: # Avoid empty strings in split text
            rand_int = np.random.randint(len(ts))
            word_to_mask = ts[rand_int]
            iter_count += 1
            if iter_count > len(ts):
                print("In the sentence <" + sen + ">, no valid words to mask.")
                give_up = True
                break
          
        if not give_up:
            # mask word
            new_text = _mask_word(sen, si[rand_int], tokenizer.mask_token)
            # get k replacement words
            top_k, included_mask = get_k_replacement_words(new_text, tokenizer, model, k=k)
            assert included_mask == True
            
            replacement_words = [tokenizer.decode([token]) for token in top_k]

            # replace mask-token with the word from the top-k replacements
            new_sentences.append([
                new_text.replace(tokenizer.mask_token, word)
                for word in replacement_words
            ])
        else:
            new_sentences.append([
                sen for _ in range(k)
            ])
    
    final_sentences = new_sentences[0]
    for sens in new_sentences[1:]:
        final_sentences = [s + a for s, a in zip(final_sentences, sens)]
    return final_sentences
	
	
def single_round(sentences: List[str], tokenizer, model, nlp, names, k) -> List[str]:
    """For a given list of sentences, do a random walk on each sentence.

    Args:
        sentences ([type]): list of sentnces to perform random walk on
        tokenizer ([type]): tokenizer
        model ([type]): model
        nlp ([type]): Spacy NLP model for finding named entities
        names (list): Named entities to not replace.
        k (int): how many words to sample to replace masked word
    Returns:
        [List]: list of k random-walked sentences
    """
    new_sentences = []

    for sentence in sentences:
        new_sentences.extend(
            single_sentence_random_step(sentence, tokenizer, model, nlp, names, k))
    return new_sentences


def random_walk(original_text: str, steps: int, k: int, tokenizer,
                model, nlp, names) -> List[str]:
    """For a sentence, perform a random walk sequence on the sentence, generating
    new sentences at each step and perturbing these during the next step.

    Args:
        original_text (str): original sentence we want to perturb
        steps (int): how many random walks iterations we perform on the sentence
        k (int): how many words to sample to replace masked word during each iteration
        tokenizer ([type]): tokenizer
        model ([type]): model
        nlp ([type]): Spacy NLP model for finding named entities
        names (bool): Whether or not to change named entities

    Returns:
        [List]: list of steps^k random-walked sentences
    """
    if names:
        doc = nlp(original_text)
        entities = [ent.text for ent in doc.ents]
        split_entities = []
        for ent in entities:
            split_iter = re.finditer(r"[\w']+|[.,!?;]", ent)
            for m in split_iter:
                split_entities.append(m.group(0))
        print('Named entities: ', split_entities)
    else:
        split_entities = []
    old_sentences = [original_text]
    # Do $steps$ steps of random walk procedure
    for _ in range(steps):
        sentences = single_round(old_sentences, tokenizer, model, nlp, split_entities, k)
        old_sentences = copy.deepcopy(sentences)
    return sentences

def sentence_similarity_metric(similarity_model, sen_A, sen_B):
    """Compute the similarity between two sentences by embedding them using a
    sentence transformer and computing the cosine similarity.

    Args:
        similarity_model (type): sentence transformer
        sen_A (str): first sentence
        sen_B (str): second sentence
    Returns:
        float: sentence similarity
    """

    emb_A = similarity_model.encode(sen_A)
    emb_B = similarity_model.encode(sen_B)

    score = util.pytorch_cos_sim(emb_A, emb_B)
    return score

class RandomWalk(SentenceOperation):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_CLASSIFICATION
    ]
    languages = ["en"]
    heavy = True
    keywords = [ "model-based", "api-based", "transformer-based", "tokenizer-required", \
        "lexical", "possible-meaning-alteration", "low-precision", \
        "high-coverage", "high-generations" ]

    # Default parameters match those of the 'test.json' below.
    def __init__(self, seed=0, max_outputs=3, steps=5, k=2, sim_req=0.25, named_entities=False):
    # For evaluation, use parameters that are less compute intensive.
    # def __init__(self, seed=0, max_outputs=1, steps=5, k=1, sim_req=0, named_entities=True):
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        super().__init__(seed, max_outputs=max_outputs)
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
        self.model = BertForMaskedLM.from_pretrained('bert-large-cased')
        self.sim_model = SentenceTransformer('all-mpnet-base-v2')
        self.spacy_nlp = spacy.load("en_core_web_sm")
        self.max_outputs = max_outputs
        self.steps = steps
        self.k = k
        self.sim_req = sim_req
        self.named_entities = named_entities

    def generate(self, sentence: str):
        print('Random walking on the sentence:', sentence)
        perturbed_texts = random_walk(
            original_text=sentence,
            steps=self.steps,
            k=self.k,
            tokenizer=self.tokenizer,
            model=self.model,
            nlp=self.spacy_nlp,
            names = self.named_entities
        )
        scores = []
        for o in perturbed_texts:
            scores.append(sentence_similarity_metric(self.sim_model, sentence, o))
        valid_sentences = np.array(scores) > self.sim_req # Only sentences with a 
        assert np.sum(valid_sentences) > 0, "Similarity requirement too high; no valid sentences. Note: Long sentences have very low similarity."
        
        # high enough similarity score are kept.
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
    #from TestRunner import convert_to_snake_case

    tf = RandomWalk(max_outputs=3, k=2, steps=5, sim_req=0.25, named_entities=True)
    #sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week.",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": "RandomWalk",#tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": "random_walk", "test_cases": test_cases} #convert_to_snake_case(tf.name())
    print(json.dumps(json_file, indent=2))

    with open('test.json', 'w') as f:
        json.dump(json_file, f, indent=2)
"""