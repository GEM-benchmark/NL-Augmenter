import random
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from indictrans import Transliterator


class MixTransliteration(SentenceOperation):
    '''
    This transformation transforms any given Indic language to it's transliterated form in english
    '''
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, source_lang:str):
        super().__init__()
        random.seed(42)
        '''
        source_lang must be from:
                   ['hin', 'guj', 'pan',
                    'ben', 'mal', 'kan', 
                    'tam', 'tel', 
                    'ori', 'eng', 
                    'mar', 'nep', 
                    'bod', 'kok',
                    'asm', 'urd']
        '''
        self.converter = Transliterator(source=source_lang, target='eng', build_lookup=True)

    def generate(self, sentence: str, prob_mix: int = 1):
        temp_text = self.converter.transform(sentence)
        temp_tokens = temp_text.split(" ")
        input_tokens = sentence.split(" ")
        output_tokens = [] 
        mixed = False # if foreign language exist,  ensures at least one is transliterated
        for i in range(len(temp_tokens)):
            if temp_tokens[i] != input_tokens[i] and (random.random() < prob_mix or mixed == False):
                output_tokens.append(temp_tokens[i])
                mixed = True
            else:
                output_tokens.append(input_tokens[i])
        output = " ".join(output_tokens)
        return [output]

