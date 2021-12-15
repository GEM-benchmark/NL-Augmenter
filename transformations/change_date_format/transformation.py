import dateparser
import numpy as np
import spacy
from babel.dates import format_date

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class DateFormatTransformation:
    nlp = None

    def __init__(self, seed=0, max_output=1):
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.max_output = max_output
        self.seed = seed

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

        # By default the parser fills the missing values with current day"s values,
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
            date = dateparser.parse(
                text, settings={"REQUIRE_PARTS": ["year", "month"]}
            )
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
        np.random.seed(self.seed)
        doc = self.nlp(input_text)
        transformed_texts = []

        for _ in range(self.max_output):
            text = input_text
            for entity in doc.ents:
                new_value = None

                if entity.label_ == "DATE":
                    date, has_year, has_month, has_day = self.parse_date(
                        entity.text
                    )

                    if date:
                        locale = np.random.choice(self.locales)
                        np.random.seed(self.seed)
                        if has_year and has_month and has_day:
                            format = np.random.choice(self.ymd_formats)
                            new_value = format_date(
                                date,
                                format=format,
                                locale=locale,
                            )
                        elif has_year and has_month:
                            format = np.random.choice(self.ym_formats)
                            new_value = format_date(
                                date,
                                format=format,
                                locale=locale,
                            )
                        elif has_month and has_day:
                            format = np.random.choice(self.md_formats)
                            new_value = format_date(
                                date,
                                format=format,
                                locale=locale,
                            )

                    if new_value:
                        text = text.replace(entity.text, str(new_value))
            transformed_texts.append(text)

        return transformed_texts


class ChangeDateFormat(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TABLE_TO_TEXT,
        TaskType.RDF_TO_TEXT,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "syntactic",
        "rule-based",
        "high-coverage",
        "high-precision",
    ]

    def __init__(self, seed=0, max_output=1):
        np.random.seed(self.seed)
        super().__init__(seed)
        self.date_format_transformation = DateFormatTransformation(
            seed, max_output
        )
        self.max_output = max_output

    def generate(self, sentence: str):
        result = self.date_format_transformation.transform(sentence)
        if self.verbose:
            print(f"Perturbed Input from {self.name()} : {result}")
        return result
