"""
# Mapping Analysis Utils

This script provides utilities to enable analysis of both transformations and filters.
@author = Saad Mahamood
"""
import json
import os

import pandas as pd

from nlaugmenter.interfaces.KeyValuePairsOperation import (
    KeyValuePairsOperation,
)
from nlaugmenter.interfaces.QuestionAnswerOperation import (
    QuestionAnswerOperation,
)
from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.interfaces.SentencePairOperation import SentencePairOperation
from nlaugmenter.interfaces.TaggingOperation import TaggingOperation


class MappingAnalysisUtilities:
    keyword_mappings = {}

    dataset = {
        "1_operation_type": [],
        "2_transformation_package_name": [],
        "3_transformation_class_name": [],
        "4_challenge_set_type": [],
        "7_task_types": [],
        "8_languages": [],
        "9_linguistic_level": [],
        "10_output_ratio": [],
        "11_input_output_cognitive_skills": [],
        "12_input_output_similarity": [],
        "13_meaning_preservation": [],
        "15_readability": [],
        "16_naturalness": [],
        "17_input_data_processing": [],
        "18_rule_model": [],
        "19_algorithm_type": [],
        "20_precision_recall": [],
    }

    def __init__(self):
        self.keyword_mappings = self.load_mappings()

    def load_mappings(self):
        keyword_mapping_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "keyword_mappings.json"
        )
        with open(keyword_mapping_file, "r") as fp:
            return json.load(fp)

    def fetch_directories(self, ignore_list: list, type: str):
        print(f"*** Fetching {type} Packages.")
        package_dir_list = []

        for root, dirs, files in os.walk(f"../{type}", topdown=False):
            for name in dirs:
                if not name.startswith("_") and os.path.isdir(
                    f"../{type}/{name}"
                ):
                    if name not in ignore_list:
                        package_dir_list.append(name)
        return package_dir_list

    def get_operation_type(self, result_obj):
        if isinstance(result_obj, KeyValuePairsOperation):
            return KeyValuePairsOperation.name()
        elif isinstance(result_obj, QuestionAnswerOperation):
            return QuestionAnswerOperation.name()
        elif isinstance(result_obj, SentenceOperation):
            return SentenceOperation.name()
        elif isinstance(result_obj, SentencePairOperation):
            return SentencePairOperation.name()
        elif isinstance(result_obj, TaggingOperation):
            return TaggingOperation.name()
        return "None"

    def build_keyword_mappings(self, operations: dict, type: str):
        print("*** Building Keyword Mappings.")
        for a_package in operations.keys():
            package_class_list = operations[a_package]

            for a_pkg_class in package_class_list:
                self.dataset["1_operation_type"].append(
                    a_pkg_class["operation_type"]
                )
                self.dataset["2_transformation_package_name"].append(a_package)
                self.dataset["3_transformation_class_name"].append(
                    a_pkg_class["class_name"]
                )
                self.dataset["4_challenge_set_type"].append(type)

                result_obj = a_pkg_class["result_obj"]
                if result_obj:
                    task_types = []
                    if result_obj.tasks:
                        for a_task in result_obj.tasks:
                            task_types.append(a_task.name)
                    self.dataset["7_task_types"].append(", ".join(task_types))

                    languages = []
                    if result_obj.languages:
                        languages = result_obj.languages
                    self.dataset["8_languages"].append(", ".join(languages))

                    keywords = []
                    if result_obj.keywords:
                        keywords = result_obj.keywords

                    for a_mapping_rule in self.keyword_mappings.keys():
                        found_keywords = []
                        mapping_keywords = self.keyword_mappings[
                            a_mapping_rule
                        ]
                        if a_mapping_rule.startswith("20_"):
                            found_precision_keyword = ""
                            found_coverage_keyword = ""
                            for a_keyword in keywords:
                                if a_keyword in mapping_keywords["precision"]:
                                    found_precision_keyword = a_keyword
                                elif a_keyword in mapping_keywords["coverage"]:
                                    found_coverage_keyword = a_keyword
                            if (
                                f"{found_precision_keyword}_{found_coverage_keyword}"
                                in mapping_keywords["mappings"]
                            ):
                                found_keywords.append(
                                    f"{found_precision_keyword}_{found_coverage_keyword}"
                                )
                        else:
                            for a_mapping_keyword in mapping_keywords.keys():
                                if a_mapping_keyword in keywords:
                                    found_keywords.append(
                                        mapping_keywords[a_mapping_keyword]
                                    )
                        self.dataset[a_mapping_rule].append(
                            self.create_mapping_keywords_text(found_keywords)
                        )

    def create_mapping_keywords_text(self, found_keywords: list):
        output_text = ", ".join(found_keywords)
        if len(found_keywords) > 1:
            output_text = "Multiple_(specify): " + output_text
        return output_text

    def generate_csv(self, type: str):
        print("*** Generating Complete CSV file.")
        output_dir_name = os.path.dirname(os.path.abspath(__file__))
        dataset_df = pd.DataFrame.from_dict(self.dataset)
        dataset_df.to_csv(
            os.path.join(
                output_dir_name, "output", type, f"{type}_dataset.csv"
            ),
            index=False,
        )
        print("*** Generating Operation Type CSV files.")
        for a_operation_type in (
            dataset_df["1_operation_type"].unique().tolist()
        ):
            operation_type_df = dataset_df.loc[
                dataset_df["1_operation_type"] == a_operation_type
            ]
            operation_type_df.to_csv(
                os.path.join(
                    output_dir_name,
                    "output",
                    type,
                    f"{type}_{(a_operation_type.lower())}_dataset.csv",
                ),
                index=False,
            )
