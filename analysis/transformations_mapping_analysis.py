"""
# Transformations Mapping Analysis

This script analyses the transformations in the
NL-Augmenter notebook and maps each transformation into specific groups using the supplied metadata.
@author = Saad Mahamood
"""
import inspect
import os
import pandas as pd
from importlib import import_module
import json

from interfaces.Operation import Operation
from interfaces.KeyValuePairsOperation import KeyValuePairsOperation
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation
from interfaces.SentencePairOperation import SentencePairOperation
from interfaces.TaggingOperation import TaggingOperation

class TransformationMappingAnalysis():
    ignore_list = ["german_gender_swap", "disability_transformation",
                   "english_inflectional_variation", "correct_common_misspellings", "ocr_perturbation",
                   "p1_noun_transformation", "summarization_transformation"]

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
        "20_precision_recall": []
    }

    def __init__(self):
        self.keyword_mappings = self.load_mappings()

    def load_mappings(self):
        keyword_mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keyword_mappings.json')
        with open(keyword_mapping_file, "r") as fp:
            return json.load(fp)

    def fetch_transformation_directories(self):
        print("*** Fetching Transformation Packages.")
        package_dir_list = []

        for root, dirs, files in os.walk("../transformations", topdown=False):
            for name in dirs:
                if not name.startswith("_") and os.path.isdir(f"../transformations/{name}"):
                    if not name in self.ignore_list:
                        package_dir_list.append(name)
        return package_dir_list

    def find_transformation_classes(self, package_dir_list: list):
        print("*** Finding Transformation Classes.")
        transformation_package = "transformations.{}.transformation"
        transformations = {}

        for a_package in package_dir_list:
            transformations[a_package] = []
            # Import the module:
            module = import_module(transformation_package.format(a_package))
            # Instantiate the object:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if issubclass(obj, Operation) and not "Operation" in name:
                        print(f"Loading: Package Name: {a_package}, Class Name: {name}")
                        result_obj = None
                        # Hardcode rules for those classes that need specific positional arguments:
                        if name == "EntityMentionReplacementNER":
                            result_obj = obj(list(), list())
                        elif name == "ButterFingersPerturbationForIL":
                            result_obj = obj("hi", "inscript")
                        elif name == "TenseTransformation":
                            result_obj = obj("random")
                        elif name == "WordNoise":
                            result_obj = obj(1, "append")
                        elif name == "MixTransliteration":
                            result_obj = obj("ar")
                        else:
                            result_obj = obj()
                        # Find out which operation type:
                        operation_type = self.get_operation_type(result_obj)
                        transformations[a_package].append({"class_name": name,
                                                           "operation_type": operation_type,
                                                           "result_obj": result_obj})
        return transformations

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

    def build_keyword_mappings(self, transformations: dict):
        print("*** Building Keyword Mappings.")
        for a_package in transformations.keys():
            package_class_list = transformations[a_package]

            for a_pkg_class in package_class_list:
                self.dataset["1_operation_type"].append(a_pkg_class["operation_type"])
                self.dataset["2_transformation_package_name"].append(a_package)
                self.dataset["3_transformation_class_name"].append(a_pkg_class["class_name"])
                self.dataset["4_challenge_set_type"].append("Transformation")

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
                        mapping_keywords = self.keyword_mappings[a_mapping_rule]
                        if a_mapping_rule.startswith("20_"):
                            found_precision_keyword = ""
                            found_coverage_keyword = ""
                            for a_keyword in keywords:
                                if a_keyword in mapping_keywords["precision"]:
                                    found_precision_keyword = a_keyword
                                elif a_keyword in mapping_keywords["coverage"]:
                                    found_coverage_keyword = a_keyword
                            if f"{found_precision_keyword}_{found_coverage_keyword}" in mapping_keywords["mappings"]:
                                found_keywords.append(f"{found_precision_keyword}_{found_coverage_keyword}")
                        else:
                            for a_mapping_keyword in mapping_keywords.keys():
                                if a_mapping_keyword in keywords:
                                    found_keywords.append(mapping_keywords[a_mapping_keyword])
                        self.dataset[a_mapping_rule].append(", ".join(found_keywords))

    def generate_csv(self):
        print("*** Generating Complete CSV file.")
        output_dir_name = os.path.dirname(os.path.abspath(__file__))
        dataset_df = pd.DataFrame.from_dict(self.dataset)
        dataset_df.to_csv(os.path.join(output_dir_name, "output", "transformations_dataset.csv"),
                          index=False)
        print("*** Generating Operation Type CSV files.")
        for a_operation_type in dataset_df["1_operation_type"].unique().tolist():
            operation_type_df = dataset_df.loc[dataset_df["1_operation_type"] == a_operation_type]
            operation_type_df.to_csv(os.path.join(output_dir_name, "output",
                                                  f"{(a_operation_type.lower())}_dataset.csv"), index=False)

def main():
    analysis = TransformationMappingAnalysis()
    package_dir_list = analysis.fetch_transformation_directories()
    transformations = analysis.find_transformation_classes(package_dir_list)
    analysis.build_keyword_mappings(transformations)
    analysis.generate_csv()


if __name__ == '__main__':
    main()
