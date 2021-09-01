import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer

from interfaces.KeyValuePairsOperation import KeyValuePairsOperation
import random
from tasks.TaskTypes import TaskType

class MRParaphrase(KeyValuePairsOperation):
    tasks = [TaskType.E2E_TASK]
    languages = ["en"]
  
    def __init__(
        self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        random.seed(0)
    
        model_name="prithivida/parrot_paraphraser_on_T5"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)  
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.max_outputs = max_outputs

    def generate(
        self, meaning_representation: dict, reference: str):
    
        outputs = []
    
        input_phrase = "paraphrase: " + reference
        input_ids = self.tokenizer.encode(input_phrase, return_tensors='pt')

        preds = self.model.generate(
            input_ids,
            do_sample=True, 
            max_length=len(reference.split()) + 10, 
            top_k=5, 
            top_p=0.95, 
            early_stopping=True,
            num_return_sequences=self.max_outputs)
    
        new_references = [self.tokenizer.decode(pred, skip_special_tokens=True) for pred in preds]
        new_references = list(set(new_references))
        return [(meaning_representation, new_ref)for new_ref in new_references]
