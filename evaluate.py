import argparse

from TestRunner import get_implementation
from evaluation.evaluation_engine import evaluate, evaluate_mt

parser = argparse.ArgumentParser(
    description="This is the evaluate function. This will evaluate your specified "
                "transformation on pre-defined models."
)
parser.add_argument("-l", "--locale", help="locale to evaluate over", default="en")
parser.add_argument("-srcl", "--src_locale", help="locale to evaluate over", default="en")
parser.add_argument("-tgtl", "--tgt_locale", help="locale to evaluate over", default="en")
parser.add_argument("--transformation", "-t", required=True)
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
  python evaluate.py -t butter_fingers_perturbation
"""
if __name__ == "__main__":
    args = parser.parse_args()

    # Identify the transformation that the user has mentioned.
    implementation = get_implementation(args.transformation)
    # Use the tasks and the locales of an implementation to retrieve an HF model and a test set.
    if len(implementation.domain()) == 2: # domain should have name and locale.
        locales = implementation.locales
        if locales != "All" and args.locale not in locales:
            raise ValueError(
                f"The specified transformation is applicable only for the locales={locales}."
            )
        evaluate(
            implementation,
            args.task_type,
            args.locale,
            args.model,
            args.dataset,
            args.percentage_of_examples,
        )
    # (2) checks for MT are here!
    elif hasattr(implementation, "src_locales") and hasattr(implementation, "tgt_locales"):
        src_locales = implementation.src_locales
        if src_locales != "All" and args.src_locale not in src_locales:
            raise ValueError(
                f"The specified transformation is applicable only for the locales={src_locales}."
            )
        tgt_locales = implementation.tgt_locales
        if tgt_locales != "All" and args.tgt_locale not in tgt_locales:
            raise ValueError(
                f"The specified transformation is applicable only for the locales={src_locales}."
            )
        evaluate_mt(
            implementation,
            args.task_type,
            args.src_locale,
            args.tgt_locale,
            args.model,
            args.dataset,
            args.percentage_of_examples,
        )
