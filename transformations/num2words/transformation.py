import re
import spacy
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import inflect 


class Numbers2Words:
    nlp = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def int2words(n, p=inflect.engine()):
        return ' '.join(p.number_to_words(n, wantlist=True, andword=' '))

    def float2words(self, float_value):
        float_value = str(round(float(float_value), 2))
        integer, dot, decimal = float_value.partition('.')
        return "{integer}{decimal}".format(
            integer=self.int2words(int(integer)),
            decimal=" and {}/100".format(decimal) if decimal and int(decimal) else '')

    def __call__(self, input_text: str):
        doc = self.nlp(input_text)

        for entity in doc.ents:
            new_value = None

            if entity.label_ == "CARDINAL" and not re.search(
                "[_]|[-]|[:]|[/]|[(]|[)]", entity.text
            ):

                cardinal_value = entity.text

                cardinal_value = cardinal_value.replace(",", "")

                if cardinal_value.isdigit() or '.' in cardinal_value:
                    cardinal_value = self.float2words(cardinal_value)
                input_text = input_text.replace(entity.text, str(cardinal_value))

        return input_text


class Num2Words(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, verbose=False):
        super().__init__(verbose=verbose)
        self.transform = Numbers2Words()

    def generate(self, sentence: str):
        result = self.transform(sentence)
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return [result]

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
if __name__ == '__main__':
    Num2Words(verbose=True).generate('she has bought hundred apples.')
    Num2Words(verbose=True).generate('she has bought 100 apples.')
    Num2Words(verbose=True).generate('she has bought 100.55 apples.')
"""