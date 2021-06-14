import pytest

from TestRunner import (
    TransformationRuns,
    get_transformation_instance,
    convert_to_camel_case,
    FilterRuns,
)
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def print_no_test_cases_found(cls_name):
    folder_name = convert_to_camel_case(cls_name)
    print(
        f"No test cases found for {cls_name}. Add a file named `test.json` in {folder_name}"
    )


def execute_sentence_operation_test_case(transformation, test_cases):
    if transformation is not None and test_cases is not None:
        for test_case in test_cases:
            output = transformation.generate(test_case["input"])
            assert (
                test_case["output"] == output
            ), f"Expected output: [{test_case['output']}] but generated: {output}"
    else:
        print_no_test_cases_found(transformation.__class__.__name__)


def execute_sentence_target_operation_test_case(transformation, test_cases):
    # interface = SentenceAndTargetOperation
    # test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test_case in test_cases:
            output_x, output_y = transformation.generate(
                test_case["input_x"], test_case["input_y"]
            )
            assert (
                output_x == test_case["output_x"]
            ), f"Expected output: {test_case['output_x']} but generated: {output_x}"
            assert (
                output_y == test_case["output_y"]
            ), f"Expected output: {test_case['output_y']} but generated: {output_y}"
    else:
        print_no_test_cases_found(transformation.__class__.__name__)


def execute_ques_ans_test_case(transformation, test_cases):
    # interface = QuestionAnswerOperation
    # test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test_case in test_cases:
            output_c, output_q, output_a = transformation.generate(
                test_case["input_c"], test_case["input_q"], test_case["input_a"]
            )
            assert (
                output_c == test_case["output_c"]
            ), f"Expected output: [{test_case['output_c']}] but generated: {output_c}"
            assert (
                output_q == test_case["output_q"]
            ), f"Expected output: [{test_case['output_q']}] but generated: {output_q}"
            assert (
                output_a == test_case["output_a"]
            ), f"Expected output: [{test_case['output_a']}] but generated: {output_a}"
    else:
        print_no_test_cases_found(transformation.__class__.__name__)


def execute_tagging_test_case(transformation, test_cases):
    if transformation is not None and test_cases is not None:
        for test_case in test_cases:
            output_sequence, output_tag = transformation.generate(
                test_case["input_sequence"].split(" "),
                test_case["input_tag"].split(" "),
            )
            assert output_sequence == test_case["output_sequence"].split(
                " "
            ), f"Expected output: [{test_case['output_sequence']}] but generated: {output_sequence}"
            assert output_tag == test_case["output_tag"].split(
                " "
            ), f"Expected output: [{test_case['output_tag']}] but generated: {output_tag}"
    else:
        print_no_test_cases_found(transformation.__class__.__name__)


def execute_test_case_for_transformation(t_test_cases):
    impl = get_transformation_instance(t_test_cases[0]["class"])
    if isinstance(impl, SentenceOperation):
        execute_sentence_operation_test_case(impl, t_test_cases)
    elif isinstance(impl, SentenceAndTargetOperation):
        execute_sentence_target_operation_test_case(impl, t_test_cases)
    elif isinstance(impl, QuestionAnswerOperation):
        execute_ques_ans_test_case(impl, t_test_cases)
    elif isinstance(impl, TaggingOperation):
        execute_tagging_test_case(impl, t_test_cases)


def test_transformations(transformation_name):
    """Entry point to run transformation test cases based on transformation_name
    transformation_name: Should be "light"/"all" or any transformation class name like 'ButterFingersPerturbation'"""
    is_heavy = False if transformation_name == "light" else True
    t_runner = (
        TransformationRuns(is_heavy)
        if transformation_name == "light" or transformation_name == "all"
        else TransformationRuns(transformation_name=transformation_name)
    )

    if len(t_runner.transformation_test_cases) == 0:
        print(f"No test cases found for {transformation_name}")
        return
    # group test-cases by class name.
    test_cases_by_class = {}
    for test_case in t_runner.transformation_test_cases:
        test_cases_by_class.setdefault(test_case["class"], []).append(test_case)

    for test_cases in test_cases_by_class.values():
        execute_test_case_for_transformation(test_cases)


def test_filters(filter_name):
    """Entry point to run filter test cases based on filter name parameter.
    filter_name: Should be "light"/"all" or any filter name"""
    tx = FilterRuns(filter_name)
    for filter, test in zip(tx.filters, tx.filter_test_cases):
        filter_args = test["inputs"]
        output = filter.filter(**filter_args)
        assert output == test["outputs"], f"The filter should return {test['outputs']}"


def main():
    pytest.main()


if __name__ == "__main__":
    main()
