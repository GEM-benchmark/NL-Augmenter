import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.mix_transliteration.transliterator import Transliterator
from typing import Optional

class MixTransliteration(SentenceOperation):
    '''
    This transformation transforms any given Indic language to it's transliterated form in english
    '''
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    langs = [
        'hin', 'guj', 'pan', 'ben', 'mal', 
        'kan', 'tam', 'tel', 'ori', 'mar', 
        'nep', 'bod', 'kok', 'asm'
    ]
    heavy = True

    def __init__(self, source_lang: str, seed: Optional[int] = 42):
        super().__init__()
        random.seed(seed)
        assert source_lang in self.langs, ValueError(f"Incorrect source language, choose from {self.langs}")
        self.converter = Transliterator(source=source_lang)

    def generate(self, sentence: str, prob_mix: int = 1):
        temp_text = self.converter.transliterate(sentence)
        temp_tokens = temp_text.split(" ")
        input_tokens = sentence.split(" ")
        output_tokens = [] 
        mixed = False # if indic script exists, ensure at least one is transliterated
        for i in range(len(temp_tokens)):
            if temp_tokens[i] != input_tokens[i] and (random.random() < prob_mix or mixed == False):
                output_tokens.append(temp_tokens[i])
                mixed = True
            else:
                output_tokens.append(input_tokens[i])
        output = " ".join(output_tokens)
        return [output]