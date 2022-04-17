"""
# Filter Mapping Analysis

This script analyses the filters in the
NL-Augmenter notebook and maps each filter into specific groups using the supplied metadata.
@author = Saad Mahamood
"""
import inspect
from importlib import import_module

from analysis.mapping_analysis_utils import MappingAnalysisUtilities
from nlaugmenter.interfaces.Operation import Operation


class FilterMappingAnalysis:
    ignore_list = []

    mapping_analysis_utils = None

    def __init__(self):
        self.mapping_analysis_utils = MappingAnalysisUtilities()

    def fetch_filter_directories(self):
        return self.mapping_analysis_utils.fetch_directories(
            ignore_list=self.ignore_list, type="filters"
        )

    def find_filter_classes(self, package_dir_list: list):
        print("*** Finding Filter Classes.")
        filter_package = "filters.{}.filter"
        filters = {}

        for a_package in package_dir_list:
            filters[a_package] = []
            # Import the module:
            module = import_module(filter_package.format(a_package))
            # Instantiate the object:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if issubclass(obj, Operation) and "Operation" not in name:
                        print(
                            f"Loading: Package Name: {a_package}, Class Name: {name}"
                        )
                        if name == "GenderBiasFilter":
                            result_obj = obj("en")
                        elif name == "PhoneticMatchFilter":
                            result_obj = obj([])
                        elif name == "SentenceAndTargetLengthFilter":
                            result_obj = obj([">", "<"], [3, 10])
                        elif name == "ToxicityFilter":
                            result_obj = obj("toxicity")
                        elif name == "GroupInequityFilter":
                            result_obj = obj(
                                "en",
                                ["she", "her", "hers"],
                                ["he", "him", "his"],
                                ["cake"],
                                ["program"],
                            )
                        elif name == "TokenAmountFilter":
                            result_obj = obj(["in", "at"], [2, 3], [">=", "<"])
                        else:
                            result_obj = obj()
                        # Find out which operation type:
                        operation_type = (
                            self.mapping_analysis_utils.get_operation_type(
                                result_obj
                            )
                        )
                        filters[a_package].append(
                            {
                                "class_name": name,
                                "operation_type": operation_type,
                                "result_obj": result_obj,
                            }
                        )
        return filters


def main():
    analysis = FilterMappingAnalysis()
    package_dir_list = analysis.fetch_filter_directories()
    transformations = analysis.find_filter_classes(package_dir_list)
    analysis.mapping_analysis_utils.build_keyword_mappings(
        operations=transformations, type="Filter"
    )
    analysis.mapping_analysis_utils.generate_csv(type="filters")


if __name__ == "__main__":
    main()
