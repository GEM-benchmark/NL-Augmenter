import spacy
import numbers

from random import *
from num2words import num2words
from word2number import w2n


from transformations.SentenceTransformation import SentenceTransformation


class ReplaceNumericalValues(SentenceTransformation):

    def __init__(self):
        self.nlp = spacy.load('en')

    def generate(self, sentence: str):
        doc = self.nlp(sentence)

        for entity in doc.ents:
            new_value = None

            if entity.label_ == "CARDINAL":
                if self.is_number(entity.text):
                    value_tens = self.value_tens_count(entity.text)

                    if isinstance(entity.text, numbers.Number):
                        new_value = randint(0, value_tens)
                    else:
                        new_value = uniform(0.0, value_tens)

                elif isinstance(entity.text, str):
                    num_value = w2n.word_to_num(entity.text)
                    value_tens = self.value_tens_count(num_value)
                    new_value = randint(0, value_tens)
                    new_value = num2words(new_value)

            if new_value:
                sentence = sentence.replace(entity.text, str(new_value))

        print(f"Perturbed Input from {self.name()} : {sentence}")
        return sentence

    def value_tens_count(self, value):
        value_text = str(value)
        value_text = value_text.split(".")[0]
        value_length = pow(10, len(value_text))

        return value_length

    def is_number(self, value):
        if isinstance(value, numbers.Number):
            return True
        else:
            try:
                float(value)
                return True
            except ValueError:
                return False
