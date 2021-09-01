import torchtext.vocab
import torch
from torchtext.data import get_tokenizer
from interfaces.KeyValuePairsOperation import KeyValuePairsOperation
import spacy
from itertools import product
import random
from random import sample
from tasks.TaskTypes import TaskType

class MRValueReplacement(KeyValuePairsOperation):
    tasks = [TaskType.E2E_TASK]
    languages = ["en"]
  
    def __init__(
        self, seed=0, n_similar=10, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

        random.seed(seed)
        self.glove = torchtext.vocab.GloVe(name = "6B", dim = "100")
        self.spacy_model = spacy.load('en_core_web_sm')
        self.max_outputs = max_outputs
        self.n_similar = n_similar

    def generate(
        self, meaning_representation: dict, reference: str):

        outputs = []
        candidate_alignments = self.get_alignments(meaning_representation, reference)

        if len(candidate_alignments) == 0:
            return outputs

        closest_set = []
        for candidate in candidate_alignments:
            closest = self.closest_words(candidate[1].lemma_.lower(), self.n_similar)

            if closest is not None:
                closest_set.append(closest)
            else:
                closest_set.append([meaning_representation[candidate[0]]])          

        if len(closest_set) == 0:
            return outputs

        products = list(product(*closest_set))
        sample_output = sample(products, self.max_outputs)

        for output_instance in sample_output:   
            mr = meaning_representation.copy()
            ref = reference
            for candidate, replacement in zip(candidate_alignments, output_instance):       
                mr[candidate[0]] = replacement
                ref = ref.replace(candidate[1].text, replacement) 
            outputs.append((mr, ref))

        return outputs
    
    def get_alignments(self, meaning_representation, reference):
    
        tokens = self.spacy_model(reference)
        candidate_alignments = []
        for key, value in meaning_representation.items():
            for token in tokens:
                if len(value.split()) == 1 and value.lower() == token.lemma_.lower():
                    candidate_alignments.append((key, token))

        return candidate_alignments
    

    def get_vector(self, word):
        if word in self.glove.stoi:
            return self.glove.vectors[self.glove.stoi[word]]
        else:
            return None
    
    def closest_words(self, word, n):
        vector = self.get_vector(word)

        if vector is None:
            return None

        distances = [(w, torch.dist(vector, self.get_vector(w)).item())
                    for w in self.glove.itos]

        return [w for w, v in sorted(distances, key = lambda w: w[1])[:n]]


