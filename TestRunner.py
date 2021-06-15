import json
import os
import inspect
import re

from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

from typing import Iterable

from interfaces.Operation import Operation
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


class OperationRuns(object):

    def __init__(self, transformation_name, search="transformations"):
        if transformation_name == 'light':
            self._load_all_transformation_test_case(heavy=False, search=search)
        elif transformation_name == 'all':
            self._load_all_transformation_test_case(heavy=True, search=search)
        else:
            self._load_single_transformation_test_case(transformation_name, search)

    def _load_single_transformation_test_case(self, transformation_name, search="transformations"):
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
            if filter_instance is None or filter_instance.name() != class_name:  # Check if already loaded
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

    @staticmethod
    def get_all_folder_names(search="transformations") -> Iterable:
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath(search)
        for (_, folder, _) in iter_modules([transformations_dir]):  # ---> ["back_translation", ...]
            yield folder

    @staticmethod
    def get_all_operations(search="transformations") -> Iterable:
        # iterate through the modules in the current package
        package_dir = Path(__file__).resolve()  # --> TestRunner.py
        transformations_dir = package_dir.parent.joinpath(search)
        for (_, folder, _) in iter_modules([transformations_dir]):  # ---> ["back_translation", ...]
            t_py = import_module(f"{search}.{folder}")
            for name, obj in inspect.getmembers(t_py):
                if inspect.isclass(obj) and issubclass(obj, Operation) \
                        and not obj.__module__.startswith("interfaces"):
                    yield obj

    @staticmethod
    def get_all_operations_for_task(query_task_type: TaskType, search="transformations") -> Iterable:
        # iterate through the modules in the current package
        for operation in OperationRuns.get_all_operations(search):
            if query_task_type in operation.tasks:
                yield operation


def get_implementation(clazz: str, search="transformations"):
    for operation in OperationRuns.get_all_operations(search):
        if operation.name() == clazz:
            return operation
    raise ValueError(f"No class called {clazz} found. Check if you've spelled it right!")


def convert_to_camel_case(word):
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def convert_to_snake_case(camel_case):
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()
    return name


if __name__ == '__main__':
    for x in OperationRuns.get_all_folder_names():
        print(x)
    for x in OperationRuns.get_all_folder_names("filters"):
        print(x)
    for x in OperationRuns.get_all_operations():
        print(x)
    for x in OperationRuns.get_all_operations("filters"):
        print(x)
    print()
    for transformation in OperationRuns.get_all_operations_for_task(TaskType.QUESTION_ANSWERING):
        print(transformation.name())
        impl = transformation()
        print(impl.generate("test", "test", ["test", "test"]))
