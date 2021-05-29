import argparse

from TestRunner import load_implementation
from evaluation.evaluation_engine import evaluate

parser = argparse.ArgumentParser(description='This is the evaluate function. This will evaluate your specified '
                                             'transformation on pre-defined models.')
parser.add_argument('-l', '--locale', help="locale to evaluate over", default="en")
parser.add_argument('--transformation', '-t', required=True)
parser.add_argument('-p', '--percentage_of_examples', help="percentage of examples to test", default=20)

if __name__ == '__main__':
    args = parser.parse_args()

    # Identify the transformation that the user has mentioned.
    implementation = load_implementation(args.transformation)
    # Use the tasks and the locales of an implementation to retrieve an HF model and a test set.
    tasks = implementation.tasks
    locales = implementation.locales
    if args.locale not in locales:
        raise Exception(f"The specified transformation is applicable only for the locales={locales}.  ")

    evaluate(implementation, args.locale, args.percentage_of_examples)
