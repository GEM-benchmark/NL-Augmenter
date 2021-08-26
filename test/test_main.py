import pytest
import random

import numpy as np

from itertools import zip_longest

from initialize import initialize_models
from interfaces.SentencePairOperation import SentencePairOperation
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import (
    SentenceAndTargetOperation,
    SentenceOperation,
)
from interfaces.TaggingOperation import TaggingOperation

from TestRunner import OperationRuns

RANDOM_SEED = 0
def reset_random_seed():
    """
    reset random seeds before tests to make them more deterministic
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    # TODO -- are there any other random seeds that should be reset here?

    
def get_assert_message(transformation, expected_output, predicted_output):
    transformation_name = transformation.__class__.__name__
    return (
        f"Mis-match in expected and predicted output for {transformation_name} transformation: \n "
        f"Expected Output: {expected_output} \n "
        f"Predicted Output: {predicted_output}"
    )


def execute_sentence_operation_test_case(transformation, test):
    reset_random_seed()
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for pred_output, output in zip_longest(perturbs, outputs):
        assert pred_output == output["sentence"], get_assert_message(
            transformation, output["sentence"], pred_output
        )


def execute_sentence_pair_operation_test_case(transformation, test):
    reset_random_seed()
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for idx, (sentence1, sentence2, target) in enumerate(perturbs):
        assert sentence1 == outputs[idx]["sentence1"], get_assert_message(
            transformation, outputs[idx]["sentence1"], sentence1
        )
        assert sentence2 == outputs[idx]["sentence2"], get_assert_message(
            transformation, outputs[idx]["sentence2"], sentence2
        )
        assert target == outputs[idx]["target"], get_assert_message(
            transformation, outputs[idx]["target"], target
        )


def execute_sentence_target_operation_test_case(transformation, test):
    reset_random_seed()
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for idx, (sentence, target) in enumerate(perturbs):
        assert sentence == outputs[idx]["sentence"], get_assert_message(
            transformation, outputs[idx]["sentence"], sentence
        )
        assert target == outputs[idx]["target"], get_assert_message(
            transformation, outputs[idx]["target"], target
        )


def execute_ques_ans_test_case(transformation, test):
    reset_random_seed()
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for idx, (context, question, answers) in enumerate(perturbs):
        assert context == outputs[idx]["context"], get_assert_message(
            transformation, outputs[idx]["context"], context
        )
        assert question == outputs[idx]["question"], get_assert_message(
            transformation, outputs[idx]["question"], question
        )
        assert answers == outputs[idx]["answers"], get_assert_message(
            transformation, outputs[idx]["answers"], answers
        )


def execute_tagging_test_case(transformation, test):
    reset_random_seed()
    filter_args = test["inputs"]
    token_sequence = filter_args["token_sequence"]
    tag_sequence = filter_args["tag_sequence"]
    outputs = test["outputs"]
    perturbs = transformation.generate(
        token_sequence.split(), tag_sequence.split()
    )
    for idx, (p_tokens, p_tags) in enumerate(perturbs):
        expected_tokens = outputs[idx]["token_sequence"].split()
        expected_tags = outputs[idx]["tag_sequence"].split()
        assert p_tokens == expected_tokens, get_assert_message(
            transformation, expected_tokens, p_tokens
        )
        assert p_tags == expected_tags, get_assert_message(
            transformation, expected_tags, p_tags
        )


def execute_test_case_for_transformation(transformation_name):
    reset_random_seed()
    print(f"Executing test cases for {transformation_name}")
    tx = OperationRuns(transformation_name)
    for transformation, test in zip(tx.operations, tx.operation_test_cases):
        print(f"Executing {transformation.name()}")
        if isinstance(transformation, SentenceOperation):
            execute_sentence_operation_test_case(transformation, test)
        elif isinstance(transformation, SentencePairOperation):
            execute_sentence_pair_operation_test_case(transformation, test)
        elif isinstance(transformation, SentenceAndTargetOperation):
            execute_sentence_target_operation_test_case(transformation, test)
        elif isinstance(transformation, QuestionAnswerOperation):
            execute_ques_ans_test_case(transformation, test)
        elif isinstance(transformation, TaggingOperation):
            execute_tagging_test_case(transformation, test)
        else:
            print(f"Invalid transformation type: {transformation}")


def execute_test_case_for_filter(filter_name):
    reset_random_seed()
    print(f"Executing test cases for {filter_name}")
    tx = OperationRuns(filter_name, "filters")
    for filter, test in zip(tx.operations, tx.operation_test_cases):
        filter_args = test["inputs"]
        output = filter.filter(**filter_args)
        assert (
                output == test["outputs"]
        ), f"Executing {test['class']} The filter should return {test['outputs']} for the inputs {test['inputs']}"


def test_operation(transformation_name, filter_name):
    reset_random_seed()
    initialize_models()
    execute_test_case_for_transformation(transformation_name)
    execute_test_case_for_filter(filter_name)


def main():
    pytest.main()


if __name__ == "__main__":
    main()
