import argparse

from TestRunner import get_implementation
from evaluation.evaluation_engine import evaluate

parser = argparse.ArgumentParser(
    description="This is the evaluate function. This will evaluate your specified "
    "transformation on pre-defined models."
)
parser.add_argument("-l", "--language", help="language to evaluate over", default="en")
parser.add_argument("--transformation", "-t", required=False)
parser.add_argument("--filter", "-f", required=False)
parser.add_argument("--task_type", "-task", help="type of the task")
parser.add_argument(
    "--model",
    "-m",
    help="HuggingFace model to evaluate. Note that the model should be in HF-models.",
)
parser.add_argument(
    "-d",
    "--dataset",
    help="Name of the HuggingFace dataset to evaluate. "
    "Note that the dataset should be in HF-datasets.",
)
parser.add_argument(
    "-p", "--percentage_of_examples", help="percentage of examples to test", default=20
)


"""
Just run this file using the following command:
  python evaluate.py -t ButterFingersPerturbation
"""


if __name__ == "__main__":
    args = parser.parse_args()

    if args.transformation is None and args.filter is None:
        raise ValueError(
            "Both transformation and filter can't be None. Either specify the name of "
            "a transformation class (-t) "
            "or a filter class (-f)"
        )

    # Identify the transformation that the user has mentioned.
    if_filter = args.transformation is None
    if args.transformation:
        implementation = get_implementation(args.transformation)
    else:
        implementation = get_implementation(args.filter, "filters")
    # Use the tasks and the locales of an implementation to retrieve an HF model and a test set.
    if True:  # domain should have name and locale.
        languages = implementation.languages
        if languages != "All" and args.language not in languages:
            raise ValueError(
                f"The specified transformation is applicable only for the locales={languages}."
            )
        evaluate(
            implementation,
            args.task_type,
            args.language,
            args.model,
            args.dataset,
            args.percentage_of_examples,
            if_filter,
        )
