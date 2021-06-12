import pytest

from TestRunner import TransformationRuns, FilterRuns, get_implementation, convert_to_camel_case
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def print_no_test_cases_found(cls_name):
    folder_name = convert_to_camel_case(cls_name)
    print(f"No test cases found for {cls_name}. Add a file named `test.json` in {folder_name}")


def execute_sentence_operation_test_case(transformation):
    interface = SentenceOperation
    test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test in test_cases:
            assert test["output"] == transformation.generate(
                test["input"]
            ), f"Should have generated {test['output']}"
    else:
        print_no_test_cases_found(transformation.name())


def execute_sentence_target_operation_test_case(transformation):
    interface = SentenceAndTargetOperation
    test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test in test_cases:
            output_x, output_y = transformation.generate(
                test["input_x"], test["input_y"]
            )
            assert (
                    output_x == test["output_x"]
            ), f"Should have generated {test['output_x']}"
            assert (
                    output_y == test["output_y"]
            ), f"Should have generated {test['output_y']}"
    else:
        print_no_test_cases_found(transformation.name())


def execute_ques_ans_test_case(transformation):
    interface = QuestionAnswerOperation
    test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test in test_cases:
            output_c, output_q, output_a = transformation.generate(
                test["input_c"], test["input_q"], test["input_a"]
            )
            assert (
                    output_c == test["output_c"]
            ), f"Should have generated {test['output_c']}"
            assert (
                    output_q == test["output_q"]
            ), f"Should have generated {test['output_q']}"
            assert (
                    output_a == test["output_a"]
            ), f"Should have generated {test['output_a']}"
    else:
        print_no_test_cases_found(transformation.name())


def execute_tagging_test_case(transformation):
    interface = TaggingOperation
    test_cases = TransformationRuns.get_test_cases(interface, implementation=transformation)
    if transformation is not None and test_cases is not None:
        for test in test_cases:
            output_sequence, output_tag = transformation.generate(
                test["input_sequence"].split(" "), test["input_tag"].split(" ")
            )
            assert (
                    output_sequence == test["output_sequence"].split(" ")
            ), f"Should have generated {test['output_sequence']}"
            assert (
                    output_tag == test["output_tag"].split(" ")
            ), f"Should have generated {test['output_tag']}"
    else:
        print_no_test_cases_found(transformation.name())


def test_transformation(transformation_name):
    if transformation_name == "light":
        print("in all")
        for tx_name in TransformationRuns.get_all_transformation_names(heavy=False):
            execute_test_case_for_transformation(tx_name)
    elif transformation_name == "all":
        for tx_name in TransformationRuns.get_all_transformation_names(heavy=True):
            execute_test_case_for_transformation(tx_name)
    else:
        execute_test_case_for_transformation(transformation_name)


def execute_test_case_for_transformation(transformation_name):
    implementation = get_implementation(transformation_name)
    impl = implementation()
    if isinstance(impl, SentenceOperation):
        execute_sentence_operation_test_case(impl)
    elif isinstance(impl, SentenceAndTargetOperation):
        execute_sentence_target_operation_test_case(impl)
    elif isinstance(impl, QuestionAnswerOperation):
        execute_ques_ans_test_case(impl)
    elif isinstance(impl, TaggingOperation):
        execute_tagging_test_case(impl)


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
