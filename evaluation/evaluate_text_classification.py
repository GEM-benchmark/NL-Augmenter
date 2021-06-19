from datasets import load_dataset
from transformers import pipeline
import numpy as np
from dataset import TextLineDataset


def evaluate(
        operation, evaluate_filter, model_name, dataset_name, split="test[:20%]"):
    # TODO: extend the task to other classification tasks that's not sentiment analysis.
    # (1) load model
    if model_name is None:
        model_name = "aychang/roberta-base-imdb"
    # (2) load test set
    if dataset_name is None:
        dataset_name = "imdb"
        fields = ["text", "label"]
    print(
        f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model.")
    text_classification_pipeline = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
    performance = {"model_name": model_name,
                   "split": split,
                   "dataset_name": dataset_name}
    if dataset_name in ["qqp", "sst2"]:
        # TODO: extend this to all the glue datasets.
        hf_dataset = load_dataset('glue', dataset_name, split=split)
        fields = ["sentence", "label"]
    else:
        hf_dataset = load_dataset(dataset_name, split=split)

    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset")

    dataset = TextLineDataset.from_huggingface(hf_dataset, ['text', 'label'])
    if evaluate_filter:
        filtered_dataset = dataset.apply_filter(operation)
        print(f"Here is the performance of the model on the filtered set")
        accuracy, total = evaluate_dataset(text_classification_pipeline, filtered_dataset)
        performance["accuracy"] = accuracy
        performance["no_of_examples"] = total
    else:
        accuracy, total = evaluate_dataset(text_classification_pipeline, dataset)
        performance["accuracy"] = accuracy
        performance["no_of_examples"] = total
        pt_dataset = dataset.apply_transformation(operation)
        print(f"Here is the performance of the model on the transformed set")
        accuracy, _ = evaluate_dataset(text_classification_pipeline, pt_dataset)
        performance["pt_accuracy"] = accuracy
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    return performance


def evaluate_dataset(text_classification_pipeline, dataset):
    def is_positive(label):
        return label == 1 or (type(label) == str and "pos" in label.lower())

    accuracy = 0
    total = 0

    for example in dataset:
        raw_text, label = example
        pred = text_classification_pipeline(raw_text, truncation=True)[0]["label"]
        if is_positive(pred) == is_positive(label):
            accuracy += 1
        total += 1

    print(f"The accuracy on this subset = {100 * accuracy / total}")
    return np.round(100 * accuracy / total, 1), total
