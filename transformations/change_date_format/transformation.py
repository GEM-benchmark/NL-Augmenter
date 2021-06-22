import random

import spacy
import dateparser

from babel.core import LOCALE_ALIASES
from babel.dates import format_date

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class DateFormatTransformation:
    nlp = None

    def __init__(self, max_output=1):
        self.nlp = spacy.load("en_core_web_sm")
        self.max_output = max_output

        self.ymd_formats = ["short", "medium", "long"]
        self.ym_formats = ["MMM Y", "MMMM Y", "MMM YY", "MMMM YY"]
        self.md_formats = [
            "d MMM",
            "d MMMM",
            "dd MMM",
            "dd MMMM",
            "MMM d",
            "MMMM d",
            "MMM dd",
            "MMMM dd",
        ]

        self.locales = [
            "en_AU",
            "en_CA",
            "en_IN",
            "en_IE",
            "en_MT",
            "en_NZ",
            "en_PH",
            "en_SG",
            "en_ZA",
            "en_GB",
            "en_US",
        ]

    def parse_date(self, text: str):
        """Parse the text to extract the date components and return a datetime object."""

        # By defualt the parser fills the missing values with current day"s values,
        # hence, using boolean values to keep track of what info is present in the text.
        date = None
        has_year = False
        has_month = False
        has_day = False

        # First check if the text contains all three parts of a date - Y, M, D.
        date = dateparser.parse(
            text, settings={"REQUIRE_PARTS": ["year", "month", "day"]}
        )

        if date is not None:
            has_year = True
            has_month = True
            has_day = True
        else:
            # Check if text contains two parts - Y and M.
            date = dateparser.parse(text, settings={"REQUIRE_PARTS": ["year", "month"]})
            if date is not None:
                has_year = True
                has_month = True
            else:
                # Check if text contains two parts - M and D.
                date = dateparser.parse(
                    text, settings={"REQUIRE_PARTS": ["month", "day"]}
                )
                if date is not None:
                    has_month = True
                    has_day = True

        return date, has_year, has_month, has_day

    def transform(self, input_text: str):
        doc = self.nlp(input_text)

        for entity in doc.ents:
            new_value = None

            if entity.label_ == "DATE":
                date, has_year, has_month, has_day = self.parse_date(entity.text)

                if date:
                    if has_year and has_month and has_day:
                        new_value = format_date(
                            date,
                            format=random.choice(self.ymd_formats),
                            locale=random.choice(self.locales),
                        )
                    elif has_year and has_month:
                        new_value = format_date(
                            date,
                            format=random.choice(self.ym_formats),
                            locale=random.choice(self.locales),
                        )
                    elif has_month and has_day:
                        new_value = format_date(
                            date,
                            format=random.choice(self.md_formats),
                            locale=random.choice(self.locales),
                        )

                if new_value:
                    input_text = input_text.replace(entity.text, str(new_value))

        return input_text


class ChangeDateFormat(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TABLE_TO_TEXT,
        TaskType.RDF_TO_TEXT,
    ]
    languages = ["en"]

    def __init__(self, max_output=1):
        random.seed(self.seed)
        super().__init__()
        self.date_format_transformation = DateFormatTransformation()
        self.max_output = max_output

    def generate(self, sentence: str):
        result = self.date_format_transformation.transform(sentence)
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return [result]


# Sample code to demonstrate usage.
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = ChangeDateFormat()
    sentences = [
        "Roger Federer (born 8 August 1981) is a Swiss professional tennis player.",
        "As of 20 June 2021, 2.66 billion doses of COVID‑19 vaccine have been administered worldwide based on official reports from national health agencies.",
        "The first known case of COVID-19 was identified in Wuhan, China in December 2019.",
        "On Feb. 25, 2021, Twitter announced Super Follows, a subscription service allowing content creators to receive payments for their content.",
        "In August 2018, Apple became the first publicly traded U.S. company to be valued at over $1 trillion.",
    ]

    test_cases = []
    for sentence in sentences:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
