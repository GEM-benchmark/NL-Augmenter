import pytest

from TestRunner import Runs, FilterRuns
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def getMessage(transformation, impl_name):
    return "For {transformation}, no transformation or test case found for {impl_name}" \
        .format(transformation=transformation, impl_name=impl_name)


def test_execute_sentence_operation_test_case(perturbation_type):
    transformation = SentenceOperation
    tx = Runs(interface=transformation, perturbation_type=perturbation_type)
    if tx.transformation is not None and tx.test_cases is not None:
        for test in tx.test_cases:
            assert test["output"] == tx.transformation.generate(
                test["input"]), f"Should have generated {test['output']}"
    else:
        print(getMessage(transformation.__name__, perturbation_type))


def test_execute_sentence_target_operation_test_case(perturbation_type):
    transformation = SentenceAndTargetOperation
    tx = Runs(interface=transformation, perturbation_type=perturbation_type)
    if tx.transformation is not None and tx.test_cases is not None:
        for test in tx.test_cases:
            output_x, output_y = tx.transformation.generate(test["input_x"], test["input_y"])
            assert output_x == test["output_x"], f"Should have generated {test['output_x']}"
            assert output_y == test["output_y"], f"Should have generated {test['output_y']}"
    else:
        print(getMessage(transformation.__name__, perturbation_type))


def test_execute_ques_ans_test_case(perturbation_type):
    transformation = QuestionAnswerOperation
    tx = Runs(interface=transformation, perturbation_type=perturbation_type)
    if tx.transformation is not None and tx.test_cases is not None:
        for test in tx.test_cases:
            output_c, output_q, output_a = tx.transformation.generate(test["input_c"], test["input_q"], test["input_a"])
            assert output_c == test["output_c"], f"Should have generated {test['output_c']}"
            assert output_q == test["output_q"], f"Should have generated {test['output_q']}"
            assert output_a == test["output_a"], f"Should have generated {test['output_a']}"
    else:
        print(getMessage(transformation.__name__, perturbation_type))


def test_execute_tagging_test_case(perturbation_type):
    transformation = TaggingOperation
    tx = Runs(interface=transformation, perturbation_type=perturbation_type)
    if tx.transformation is not None and tx.test_cases is not None:
        for test in tx.test_cases:
            output_sequence, output_tag = tx.transformation.generate(test["input_sequence"], test["input_tag"])
            assert output_sequence == test["output_sequence"], f"Should have generated {test['output_sequence']}"
            assert output_tag == test["output_tag"], f"Should have generated {test['output_tag']}"
    else:
        print(getMessage(transformation.__name__, perturbation_type))


def test_execute_filter_test_case():
    tx = FilterRuns()
    for filter, test in zip(tx.filters, tx.filter_test_cases):
        filter_args = test["filter_args"]
        output = filter.filter(**filter_args)
        assert output == test["output"], f"The filter should return {test['output']}"
            


def main():
    pytest.main()


if __name__ == "__main__":
    main()
