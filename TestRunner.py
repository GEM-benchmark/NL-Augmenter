import json
import os
import inspect
import re

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

from typing import Iterable
from tasks.TaskTypes import TaskType


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
        raise Exception(
            f"\n\n\t\tYou should add a test file at this location!\n\t\t{test_json}"
        )


class TransformationRuns(object):
    def __init__(self, interface, name_of_transformation, load_tests=True):
        self.transformation = None
        self.test_cases = None
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath("transformations")
        for (_, m, _) in iter_modules([transformations_dir]):
            if m == name_of_transformation:
                t_py = import_module(f"transformations.{m}.transformation")
                for cls in interface.__subclasses__():
                    if hasattr(t_py, cls.__name__):
                        self.transformation = load(t_py, cls)
                        if load_tests:
                            t_js = os.path.join(transformations_dir, m, "test.json")
                            self.test_cases = load_test_cases(t_js)
                        break
                break

    @staticmethod
    def get_test_cases(interface, implementation):
        name_of_transformation = convert_to_snake_case(implementation.name())
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath("transformations")
        for (_, m, _) in iter_modules([transformations_dir]):
            if m == name_of_transformation:
                t_py = import_module(f"transformations.{m}.transformation")
                for cls in interface.__subclasses__():
                    if hasattr(t_py, cls.__name__):
                        t_js = os.path.join(transformations_dir, m, "test.json")
                        return load_test_cases(t_js)
                break

    # bit of cleanup required, filters need to be added.
    @staticmethod
    def get_all_transformations_for_task(query_task_type: TaskType) -> Iterable:
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath("transformations")
        for (_, m, _) in iter_modules([transformations_dir]):
            t_py = import_module(f"transformations.{m}.transformation")
            for name, obj in inspect.getmembers(t_py):
                if inspect.isclass(obj) and hasattr(obj, "tasks"):
                    tasks = obj.tasks
                    if tasks is not None and query_task_type in tasks:
                        yield load(t_py, obj)

    @staticmethod
    def get_all_transformation_names(heavy=False) -> Iterable:
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath("transformations")
        for (_, m, _) in iter_modules([transformations_dir]): # ---> ["back_translation", ...]
            t_py = import_module(f"transformations.{m}.transformation")
            for name, obj in inspect.getmembers(t_py):
                if convert_to_camel_case(m) == name:
                    if inspect.isclass(obj) and hasattr(obj, "heavy"):
                        is_heavy = obj.is_heavy()
                        if not is_heavy:
                            yield m
                        else:
                            if heavy:
                                yield m


class TransformationRuns2(object):

    def __init__(self, transformation_name, search="transformations"):
        if transformation_name == 'light':
            self._load_all_transformation_test_case(heavy=False, search=search)
        elif transformation_name == 'all':
            self._load_all_transformation_test_case(heavy=True, search=search)
        else:
            self._load_single_transformation_test_case(transformation_name, search)

    def _load_single_transformation_test_case(self, transformation_name,  search="transformations"):
        filters = []
        filter_test_cases = []
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        filters_dir = package_dir.parent.joinpath(search, transformation_name)

        t_py = import_module(f"{search}.{transformation_name}")
        t_js = os.path.join(filters_dir, "test.json")
        filter_instance = None
        for test_case in load_test_cases(t_js):
            class_name = test_case["class"]
            class_args = test_case["args"] if "args" in test_case else {}
            # construct filter class with input args
            cls = getattr(t_py, class_name)
            if filter_instance is None or filter_instance.name() != class_name: # Check if already loaded
                filter_instance = cls(**class_args)
            filters.append(filter_instance)
            filter_test_cases.append(test_case)

        self.operations = filters
        self.operation_test_cases = filter_test_cases

    def _load_all_transformation_test_case(self, heavy=False, search="transformations"):
        filters = []
        filter_test_cases = []
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        filters_dir = package_dir.parent.joinpath(search)
        for (_, m, _) in iter_modules([filters_dir]):
            t_py = import_module(f"{search}.{m}")
            t_js = os.path.join(filters_dir, m, "test.json")
            filter_instance = None
            for test_case in load_test_cases(t_js):
                class_name = test_case["class"]
                class_args = test_case["args"] if "args" in test_case else {}
                cls = getattr(t_py, class_name)

                is_heavy = cls.is_heavy()
                if (not heavy) and is_heavy:
                    continue
                else:
                    if filter_instance is None or filter_instance.name() != class_name:  # Check if already loaded
                        filter_instance = cls(**class_args)

                    filters.append(filter_instance)
                    filter_test_cases.append(test_case)

        self.operations = filters
        self.operation_test_cases = filter_test_cases


def get_implementation(tx_name: str):
    try:
        t_py = import_module(f"transformations.{tx_name}.transformation")
    except ModuleNotFoundError as error:
        raise Exception(
            f"Transformation folder of name {tx_name} is not found. Make sure you've spelt it correctly!\n {error}"
        )
    TxName = convert_to_camel_case(tx_name)
    try:
        transformation = getattr(t_py, TxName)
        return transformation
    except AttributeError as error:
        raise Exception(
            f"Transformation implementation" f" named {TxName} not found.\n {error}"
        )


def convert_to_camel_case(word):
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def convert_to_snake_case(camel_case):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()
    return name


if __name__ == '__main__':
    for tx in TransformationRuns.get_all_transformation_names(True):
        print(tx)
    for transformation in TransformationRuns.get_all_transformations_for_task(TaskType.TEXT_CLASSIFICATION):
        print(transformation.generate("This is a quick test code to show all the transformations "
                                      "for a particular task type!"))
