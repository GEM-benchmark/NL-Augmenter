from itertools import zip_longest
from test.keywords import keywords_in_file

import pytest

from nlaugmenter.evaluation.TestRunner import OperationRuns
from nlaugmenter.interfaces.KeyValuePairsOperation import (
    KeyValuePairsOperation,
)
from nlaugmenter.interfaces.QuestionAnswerOperation import (
    QuestionAnswerOperation,
)
from nlaugmenter.interfaces.SentenceOperation import (
    SentenceAndTargetOperation,
    SentenceOperation,
)
from nlaugmenter.interfaces.SentencePairOperation import SentencePairOperation
from nlaugmenter.interfaces.TaggingOperation import TaggingOperation
from nlaugmenter.utils.initialize import initialize_models, reinitialize_spacy

expected_keywords = keywords_in_file()


def get_assert_message(transformation, expected_output, predicted_output):
    transformation_name = transformation.__class__.__name__
    return (
        f"Mismatch in expected and predicted output for {transformation_name} transformation: \n "
        f"Expected Output: {expected_output} \n "
        f"Predicted Output: {predicted_output}"
    )


def execute_sentence_operation_test_case(transformation, test):
    filter_args = test["inputs"]
    outputs = test["outputs"]
    perturbs = transformation.generate(**filter_args)
    for pred_output, output in zip_longest(perturbs, outputs):
        assert pred_output == output["sentence"], get_assert_message(
            transformation, output["sentence"], pred_output
        )


def execute_sentence_pair_operation_test_case(transformation, test):
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


def execute_key_value_pair_test_case(transformation, test):
    filter_args = test["inputs"]
    mr = filter_args["meaning_representation"]
    reference = filter_args["reference"]
    outputs = test["outputs"]
    perturbs = transformation.generate(mr, reference)
    for idx, (p_mr, p_ref) in enumerate(perturbs):
        print(p_mr)
        expected_mr = outputs[idx]["meaning_representation"]
        expected_ref = outputs[idx]["reference"]
        assert p_mr == expected_mr, get_assert_message(
            transformation, expected_mr, p_mr
        )
        assert p_ref == expected_ref, get_assert_message(
            transformation, expected_ref, p_ref
        )


def assert_keywords(transformation):
    print("Checking for keywords")
    keywords_t = transformation.keywords
    if (
        keywords_t is not None
    ):  # TODO: later remove this as soon as all transformations have keywords
        assert keywords_t is not None and len(keywords_t) > 0, (
            f"Keywords of {transformation.name()} " f"should not be empty"
        )
        assert set(keywords_t) < set(expected_keywords), (
            f"Some Keywords in {transformation.name()} "
            f"not present in docs/keywords.md file "
            f": {set(keywords_t) - set(expected_keywords)} "
        )


def execute_test_case_for_transformation(transformation_name):
    print(f"Executing test cases for {transformation_name}")
    tx = OperationRuns(transformation_name)
    for transformation, test in zip(tx.operations, tx.operation_test_cases):
        assert_keywords(transformation)
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
        elif isinstance(transformation, KeyValuePairsOperation):
            execute_key_value_pair_test_case(transformation, test)
        else:
            print(f"Invalid transformation type: {transformation}")
        # Reinitialize spacy tokenizer [TODO: Need to run only for transformations using spacy]
        reinitialize_spacy()


def execute_test_case_for_filter(filter_name):
    print(f"Executing test cases for {filter_name}")
    tx = OperationRuns(filter_name, "filters")
    for filter, test in zip(tx.operations, tx.operation_test_cases):
        assert_keywords(filter)
        filter_args = test["inputs"]
        output = filter.filter(**filter_args)
        assert (
            output == test["outputs"]
        ), f"Executing {test['class']} The filter should return {test['outputs']} for the inputs {test['inputs']}"


def test_operation(transformation_name, filter_name):
    initialize_models()
    execute_test_case_for_transformation(transformation_name)
    execute_test_case_for_filter(filter_name)


def main():
    pytest.main()


if __name__ == "__main__":
    main()
