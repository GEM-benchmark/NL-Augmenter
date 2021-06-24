import pytest

from TestRunner import OperationRuns
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation, SentenceAndTargetOperation
from interfaces.TaggingOperation import TaggingOperation


def execute_sentence_operation_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for pred_output, output in zip(perturbs, outputs):
        assert pred_output == output["sentence"]


def execute_sentence_target_operation_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for idx, (sentence, target) in enumerate(perturbs):
        assert sentence == outputs[idx]["sentence"]
        assert target == outputs[idx]["target"]


def execute_ques_ans_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for idx, (context, question, answers) in enumerate(perturbs):
        assert context == outputs[idx]["context"]
        assert question == outputs[idx]["question"]
        assert answers == outputs[idx]["answers"]


def execute_tagging_test_case(transformation, test):
    filter_args = test["inputs"]
    token_sequence = filter_args["token_sequence"]
    tag_sequence = filter_args["tag_sequence"]
    outputs = test["outputs"]
    perturbs = transformation.generate(
        token_sequence.split(" "), tag_sequence.split(" ")
    )
    for idx, (p_tokens, p_tags) in enumerate(perturbs):
        assert p_tokens == outputs[idx]["token_sequence"].split(" ")
        assert p_tags == outputs[idx]["tag_sequence"].split(" ")


def execute_test_case_for_transformation(transformation_name):
    tx = OperationRuns(transformation_name)
    for transformation, test in zip(tx.operations, tx.operation_test_cases):
        if isinstance(transformation, SentenceOperation):
            execute_sentence_operation_test_case(transformation, test)
        elif isinstance(transformation, SentenceAndTargetOperation):
            execute_sentence_target_operation_test_case(transformation, test)
        elif isinstance(transformation, QuestionAnswerOperation):
            execute_ques_ans_test_case(transformation, test)
        elif isinstance(transformation, TaggingOperation):
            execute_tagging_test_case(transformation, test)
        else:
            print(f"Invalid transformation type: {transformation}")


def execute_test_case_for_filter(filter_name):
    tx = OperationRuns(filter_name, "filters")
    for filter, test in zip(tx.operations, tx.operation_test_cases):
        filter_args = test["inputs"]
        output = filter.filter(**filter_args)
        assert output == test["outputs"], f"The filter should return {test['outputs']}"


def test_operation(transformation_name, filter_name):
    execute_test_case_for_transformation(transformation_name)
    execute_test_case_for_filter(filter_name)


def main():
    pytest.main()


if __name__ == "__main__":
    main()
