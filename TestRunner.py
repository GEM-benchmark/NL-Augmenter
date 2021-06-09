import json
import os

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules


def load(module, cls):
    my_class = getattr(module, cls.__name__)
    return my_class()


def load_test_cases(test_json):
    try:
        with open(test_json) as f:
            d = json.load(f)
            examples = d["test_cases"]
        return examples
    except FileNotFoundError:
        raise Exception(f"\n\n\t\tYou should add a test file at this location!\n\t\t{test_json}")


class Runs(object):

    def __init__(self, interface, perturbation_type, load_tests=True):
        self.transformation = None
        self.test_cases = None
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath("transformations")
        for (_, m, _) in iter_modules([transformations_dir]):
            if m == perturbation_type:
                t_py = import_module(f"transformations.{m}.transformation")
                t_js = os.path.join(transformations_dir, m, "test.json")
                for cls in interface.__subclasses__():
                    if hasattr(t_py, cls.__name__):
                        self.transformation = load(t_py, cls)
                        if load_tests:
                            self.test_cases = load_test_cases(t_js)
                        break
                break

class FilterRuns(object):
    
    def __init__(self):
        filters = []
        filter_test_cases = []
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        filters_dir = package_dir.parent.joinpath("filters")
        for (_, m, _) in iter_modules([filters_dir]):  
            t_py = import_module(f"filters.{m}")
            t_js = os.path.join(filters_dir, m, "test.json")
            
            for test_case in load_test_cases(t_js):
                class_name = test_case['class']
                class_args = test_case['args']
                # construct filter class with input args         
                cls = getattr(t_py, class_name)
                filter_instance = cls(**class_args)
                
                filters.append(filter_instance)
                filter_test_cases.append(test_case)
            
        self.filters = filters
        self.filter_test_cases = filter_test_cases

def load_implementation(tx_name: str):
    try:
        t_py = import_module(f"transformations.{tx_name}.transformation")
    except ModuleNotFoundError as error:
        raise Exception(f"Transformation folder of name {tx_name} is not found.\n {error}")
    TxName = convert_to_camel_case(tx_name)
    try:
        transformation = getattr(t_py, TxName)
        return transformation
    except AttributeError as error:
        raise Exception(f"Transformation implementation"
                        f" named {TxName} not found.\n {error}")


def convert_to_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))
