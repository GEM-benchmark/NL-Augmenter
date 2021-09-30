from evaluation import (
    evaluate_ner_tagging,
    evaluate_text_generation,
    evaluate_question_answering,
    evaluate_text_classification,
)
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
This is the evaluation engine.
Currently has been implemented for SentenceTransformation:
eg. python evaluate.py -t ButterFingersPerturbation
"""


def evaluate(
    implementation,
    task_type,
    language="en",
    model=None,
    dataset=None,
    percentage_of_examples=None,
    evaluate_filter=False,
):
    # The evaluation engine would effectively do the following
    # (1) Loading a standard model and a test set (the model's original test set would be the best choice)
    # (2) Executing perturbations to generate the perturbed test set.
    # (3) Executing these against the model and evaluate its performance (display nicely :P )
    # (4) Writing a neat README.
    task_type = get_task_type(implementation, task_type)
    execute_model(
        implementation,
        evaluate_filter=evaluate_filter,
        task_type=task_type,
        locale=language,
        model_name=model,
        dataset=dataset,
        percentage_of_examples=percentage_of_examples,
    )
    return


def evaluate_mt(
    implementation,
    task_type,
    src_locale="en",
    tgt_locale="en",
    model=None,
    dataset=None,
    percent_of_examples=None,
    evaluate_filter=False,
):
    # TODO
    return


def get_task_type(implementation, task_type):
    if task_type is None:
        print(
            "Undefined task type, switching to default task %s",
            implementation.tasks[0].name,
        )
        return str(implementation.tasks[0]).split(".")[1]
    return task_type


def execute_model(
    implementation,
    task_type,
    locale="en",
    model_name=None,
    dataset=None,
    percentage_of_examples=20,
    evaluate_filter=False,
):
    interface = implementation.__bases__[0]  # SentenceTransformation
    impl = implementation()
    if locale in ("en", "zh"):
        if (
            isinstance(impl, SentenceOperation)
            and TaskType[task_type] == TaskType.TEXT_CLASSIFICATION
        ):
            return evaluate_text_classification.evaluate(
                impl,
                evaluate_filter,
                model_name,
                dataset,
                split=f"test[:{percentage_of_examples}%]",
            )

        elif (
            isinstance(impl, QuestionAnswerOperation)
            and TaskType[task_type] == TaskType.QUESTION_ANSWERING
        ):
            return evaluate_question_answering.evaluate(
                impl,
                evaluate_filter,
                model_name,
                dataset,
                split=f"validation[:{percentage_of_examples}%]",
            )

        elif (
            isinstance(impl, SentenceOperation)
            and TaskType[task_type] == TaskType.TEXT_TO_TEXT_GENERATION
        ):
            return evaluate_text_generation.evaluate(
                impl,
                evaluate_filter,
                model_name,
                dataset,
                split=f"test[:{percentage_of_examples}%]",
            )

        elif (
            isinstance(impl, TaggingOperation)
            and TaskType[task_type] == TaskType.TEXT_TAGGING
        ):
            return evaluate_ner_tagging.evaluate(
                impl,
                evaluate_filter,
                model_name,
                dataset,
                split=f"test[:{percentage_of_examples}%]",
            )
        # Other if else cases should be added here.
        else:
            print(
                f"No default evaluation model exists for the interface {interface} in the locale {locale}."
                f"It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate "
                f"your perturbation on a task and a dataset, "
                f"the right place to do it would to add a new class in the evaluation folder "
                f"and call it from execute_model. That's it!"
            )
    else:
        print(
            f"No default evaluation model exists in the locale {locale}."
            f"It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate "
            f"your perturbation on a task and a dataset, "
            f"the right place to do it would to add a new class in the evaluation folder "
            f"and call it from execute_model. That's it!"
        )
