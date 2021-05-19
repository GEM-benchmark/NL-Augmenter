import unittest

from TestRunner import Runs
from interfaces.SentenceTransformation import SentenceTransformation, SentenceAndTargetTransformation


def execute_test_cases_1():
    tx = Runs(interface=SentenceTransformation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            assert test["output"] == transformation.generate(test["input"]), f"Should have generated {test['output']}"


def execute_test_cases_2():
    tx = Runs(interface=SentenceAndTargetTransformation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            output_x, output_y = transformation.generate(test["input_x"], test["input_y"])
            assert output_x == test["output_x"], f"Should have generated {test['output_x']}"
            assert output_y == test["output_y"], f"Should have generated {test['output_y']}"


class TestStringMethods(unittest.TestCase):

    def test_1(self):
        execute_test_cases_1()

    def test_2(self):
        execute_test_cases_2()


if __name__ == '__main__':
    unittest.main()
