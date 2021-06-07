import argparse
import logging

from TestRunner import load_implementation
from evaluation.evaluation_engine import evaluate

parser = argparse.ArgumentParser(description='This is the evaluate function. This will evaluate your specified '
                                             'transformation on pre-defined models.')
parser.add_argument('-l', '--locale', help="locale to evaluate over", default="en")
parser.add_argument('--transformation', '-t', required=True)
parser.add_argument('--task_type', '-task', help="type of the task")
parser.add_argument('--model', '-m', help="HuggingFace model to evaluate. Note that the model should be in HF-models.")
parser.add_argument('-d', '--dataset', help="Name of the HuggingFace dataset to evaluate. "
                                            "Note that the dataset should be in HF-datasets.")
parser.add_argument('-p', '--percentage_of_examples', help="percentage of examples to test", default=20)

"""
Just run this file using the following command:
  python evaluate.py -t butter_fingers_perturbation
"""
if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    # Identify the transformation that the user has mentioned.
    implementation = load_implementation(args.transformation)
    # Use the tasks and the locales of an implementation to retrieve an HF model and a test set.
    locales = implementation.locales
    if locales != "All" and args.locale not in locales:
        raise ValueError(f"The specified transformation is applicable only for the locales={locales}.")

    evaluate(implementation, args.task_type, args.locale, args.model, args.dataset, args.percentage_of_examples)
