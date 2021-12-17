"""
# Transformations Mapping Analysis

This script analyses the transformations in the
NL-Augmenter notebook and maps each transformation into specific groups using the supplied metadata.
@author = Saad Mahamood
"""
import inspect
from importlib import import_module

from analysis.mapping_analysis_utils import MappingAnalysisUtilities
from nlaugmenter.interfaces.Operation import Operation


class TransformationMappingAnalysis:
    ignore_list = [
        "german_gender_swap",
        "disability_transformation",
        "english_inflectional_variation",
        "correct_common_misspellings",
        "ocr_perturbation",
        "p1_noun_transformation",
        "summarization_transformation",
    ]

    mapping_analysis_utils = None

    def __init__(self):
        self.mapping_analysis_utils = MappingAnalysisUtilities()

    def fetch_transformation_directories(self):
        return self.mapping_analysis_utils.fetch_directories(
            ignore_list=self.ignore_list, type="transformations"
        )

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
                    if issubclass(obj, Operation) and "Operation" not in name:
                        print(
                            f"Loading: Package Name: {a_package}, Class Name: {name}"
                        )
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
                        operation_type = (
                            self.mapping_analysis_utils.get_operation_type(
                                result_obj
                            )
                        )
                        transformations[a_package].append(
                            {
                                "class_name": name,
                                "operation_type": operation_type,
                                "result_obj": result_obj,
                            }
                        )
        return transformations


def main():
    analysis = TransformationMappingAnalysis()
    package_dir_list = analysis.fetch_transformation_directories()
    transformations = analysis.find_transformation_classes(package_dir_list)
    analysis.mapping_analysis_utils.build_keyword_mappings(
        operations=transformations, type="Transformation"
    )
    analysis.mapping_analysis_utils.generate_csv(type="transformations")


if __name__ == "__main__":
    main()
