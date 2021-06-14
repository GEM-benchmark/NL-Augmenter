import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import spacy
import numbers
import re
from fractions import Fraction
from num2words import num2words
from word2number import w2n


class NumericalTransformation:
    nlp = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def transform(self, input_text: str):
        doc = self.nlp(input_text)

        for entity in doc.ents:
            new_value = None

            if entity.label_ == "CARDINAL" and not re.search(
                "[_]|[-]|[:]|[/]|[(]|[)]", entity.text
            ):
                # Flag if the value has formatting:
                has_formatting = False
                is_fraction = False

                if entity.text.find(",") > -1:
                    has_formatting = True

                if entity.text.find("/") > -1:
                    is_fraction = True

                cardinal_value = entity.text

                # Remove numerical formatting:
                cardinal_value = cardinal_value.replace(",", "")

                # Convert Fraction to float:
                if is_fraction:
                    tokens = cardinal_value.split("/")
                    if len(tokens) == 2:
                        cardinal_value = int(tokens[0]) / int(tokens[1])

                if self.is_number(cardinal_value):
                    value_tens = self.value_tens_count(cardinal_value)

                    if isinstance(cardinal_value, numbers.Number):
                        new_value = random.randint(0, value_tens)
                    else:
                        new_value = random.uniform(0.0, value_tens)
                        # Format value to same number of floating point values:
                        split_entity_value_list = cardinal_value.split(".")
                        floating_length = 0
                        if len(split_entity_value_list) > 1:
                            floating_length = len(split_entity_value_list[1])
                        new_value = "%.{}f".format(floating_length) % new_value

                        if is_fraction:
                            new_value = str(Fraction(float(new_value)))

                    if has_formatting:
                        if float(new_value).is_integer():
                            new_value = "{:,}".format(int(new_value))
                        else:
                            new_value = "{:,}".format(float(new_value))

                elif isinstance(cardinal_value, str):
                    try:
                        num_value = w2n.word_to_num(cardinal_value)
                        value_tens = self.value_tens_count(num_value)
                        new_value = random.randint(0, value_tens)
                        new_value = num2words(new_value)
                    except ValueError:
                        print(
                            "Value: {} is not recognised as an alpha-number".format(
                                cardinal_value
                            )
                        )

            if new_value:
                input_text = input_text.replace(entity.text, str(new_value))

        return input_text

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


class ReplaceNumericalValues(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self):
        random.seed(self.seed)
        super().__init__()
        self.numerical_transformation = NumericalTransformation()

    def generate(self, sentence: str):
        result = self.numerical_transformation.transform(sentence)
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return result
