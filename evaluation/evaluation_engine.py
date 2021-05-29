from datasets import load_dataset
from transformers import pipeline

"""
This is the evaluation engine.
Currently has been implemented for SentenceTransformation:
eg. python evaluate.py -t butter_fingers_perturbation
"""


def evaluate(implementation, locale, percent_of_examples):
    # The evaluation engine would effectively do the following
    # (1) Loading a standard model and a test set (the model's original test set would be the best choice)
    # (2) Executing perturbations to generate the perturbed test set.
    # (3) Executing these against the model and evaluate its performance (display nicely :P )
    # (4) Writing a neat README.
    interface = implementation.__bases__[0]  # SentenceTransformation
    impl = implementation()
    percent_of_examples = percent_of_examples if percent_of_examples is not None else 100
    execute_model(impl, interface, locale, percent_of_examples)
    return


def evaluate_text_classifier(transformation, split='test[:20%]'):
    # (1) load model
    model_name = "aychang/roberta-base-imdb"
    # (2) load test set
    dataset_name = 'imdb'
    dataset = load_dataset(dataset_name, split=split)
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    nlp = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
    accuracy = 0
    pt_accuracy = 0
    total = 0
    for example in dataset:
        label = example["label"]
        pred = nlp(example["text"], truncation=True)[0]["label"]
        if (pred == "pos" and label == 1) or (pred == "neg" and label == 0):
            accuracy += 1
        pt = transformation.generate(example["text"])
        pt_pred = nlp(pt, truncation=True)[0]["label"]
        if (pt_pred == "pos" and label == 1) or (pt_pred == "neg" and label == 0):
            pt_accuracy += 1
        total += 1
    print(f"The accuracy on a subset of {dataset_name} = {100 * accuracy / total}")
    print(f"The accuracy on its perturbed set generated from = {100 * pt_accuracy / total}")


def execute_model(impl, interface, locale, percentage_of_examples):
    if interface.__name__ is "SentenceTransformation" and locale is "en":
        evaluate_text_classifier(impl, f'test[:{percentage_of_examples}%]')
    elif interface.__name__ is "SentenceAndTargetTransformation" and locale is "en":
        print("To be added.")
    # Other if else cases should be added here.
