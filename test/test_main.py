import pytest

from TestRunner import convert_to_camel_case, TransformationRuns2
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def print_no_test_cases_found(cls_name):
    folder_name = convert_to_camel_case(cls_name)
    print(f"No test cases found for {cls_name}. Add a file named `test.json` in {folder_name}")


def execute_sentence_operation_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    output = transformation.generate(**filter_args)
    assert output == outputs["sentence"]


def execute_sentence_target_operation_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    output, target = transformation.generate(**filter_args)
    assert output == outputs["sentence"]
    assert target == outputs["target"]


def execute_ques_ans_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    context, question, answers = transformation.generate(**filter_args)
    assert context == outputs["context"]
    assert question == outputs["question"]
    assert answers == outputs["answers"]


def execute_tagging_test_case(transformation, test):
    filter_args = test["inputs"]
    token_sequence = filter_args["token_sequence"]
    tag_sequence = filter_args["tag_sequence"]
    outputs = test["outputs"]
    output, tags = transformation.generate(token_sequence.split(" "), tag_sequence.split(" "))
    assert output == outputs["token_sequence"].split(" ")
    assert tags == outputs["tag_sequence"].split(" ")


def test_operation(transformation_name, filter_name):
    execute_test_case_for_transformation(transformation_name)
    execute_test_case_for_filter(filter_name)
        

def execute_test_case_for_transformation(transformation_name):
    tx = TransformationRuns2(transformation_name)
    for transformation, test in zip(tx.operations, tx.operation_test_cases):
        if isinstance(transformation, SentenceOperation):
            execute_sentence_operation_test_case(transformation, test)
        elif isinstance(transformation, SentenceAndTargetOperation):
            execute_sentence_target_operation_test_case(transformation, test)
        elif isinstance(transformation, QuestionAnswerOperation):
            execute_ques_ans_test_case(transformation, test)
        elif isinstance(transformation, TaggingOperation):
            execute_tagging_test_case(transformation, test)


def execute_test_case_for_filter(filter_name):
    tx = TransformationRuns2(filter_name, "filters")
    for filter, test in zip(tx.operations, tx.operation_test_cases):
        filter_args = test["inputs"]
        output = filter.filter(**filter_args)
        assert output == test["outputs"], f"The filter should return {test['outputs']}"


def main():
    pytest.main()


if __name__ == "__main__":
    main()
