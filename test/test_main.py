import unittest

from TestRunner import Runs
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def execute_test_cases_1():
    tx = Runs(interface=SentenceOperation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            assert test["output"] == transformation.generate(test["input"]), f"Should have generated {test['output']}"


def execute_test_cases_2():
    tx = Runs(interface=SentenceAndTargetOperation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            output_x, output_y = transformation.generate(test["input_x"], test["input_y"])
            assert output_x == test["output_x"], f"Should have generated {test['output_x']}"
            assert output_y == test["output_y"], f"Should have generated {test['output_y']}"


def execute_test_cases_3():
    tx = Runs(interface=QuestionAnswerOperation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            output_c, output_q, output_a = transformation.generate(test["input_c"], test["input_q"], test["input_a"])
            assert output_c == test["output_c"], f"Should have generated {test['output_c']}"
            assert output_q == test["output_q"], f"Should have generated {test['output_q']}"
            assert output_a == test["output_a"], f"Should have generated {test['output_a']}"


def execute_test_cases_4():
    tx = Runs(interface=TaggingOperation)
    for transformation, tests in zip(tx.transformations, tx.test_cases):
        for test in tests:
            output_sequence, output_tag = transformation.generate(test["input_sequence"], test["input_tag"])
            assert output_sequence == test["output_sequence"], f"Should have generated {test['output_sequence']}"
            assert output_tag == test["output_tag"], f"Should have generated {test['output_tag']}"


class TestStringMethods(unittest.TestCase):

    def test_1(self):
        execute_test_cases_1()

    def test_2(self):
        execute_test_cases_2()

    def test_3(self):
        execute_test_cases_3()

    def test_4(self):
        execute_test_cases_4()


if __name__ == '__main__':
    unittest.main()
