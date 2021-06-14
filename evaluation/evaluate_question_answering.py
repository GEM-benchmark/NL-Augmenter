from datasets import load_dataset
from pandas import np
from transformers import pipeline

from dataset import KeyValueDataset
from tasks.TaskTypes import TaskType


def evaluate(operation, model_name, dataset_name, split="validation[:20%]", evaluate_filter=False):
    # (1) load model
    if model_name is None:
        model_name = "mrm8488/bert-tiny-5-finetuned-squadv2"
    # (2) load test set
    if dataset_name is None:
        dataset_name = "squad"
    print(
        f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model.")

    hf_dataset = load_dataset(dataset_name, split=split)
    qa_pipeline = pipeline("question-answering", model=model_name, tokenizer=model_name)

    dataset = KeyValueDataset.from_huggingface(
        hf_dataset, TaskType.QUESTION_ANSWERING, ['context', 'question', 'answers'])

    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )

    if evaluate_filter:
        filtered_dataset =  dataset.apply_filter(operation)
        print(f"Starting evaluation on the filtered dataset.")
        performance = evaluate_on_dataset(filtered_dataset, qa_pipeline)
    else:
        print(f"Starting evaluation on the original dataset.")
        performance = evaluate_on_dataset(dataset, qa_pipeline)

        print(f"Starting evaluation on the transformed dataset.")
        pt_dataset = dataset.apply_transformation(operation)
        pt_performance = evaluate_on_dataset(pt_dataset, qa_pipeline)
        performance["pt_accuracy"] = pt_performance["accuracy"]

    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set

    performance["model_name"] = model_name
    performance["split"] = split
    performance["dataset_name"] = dataset_name

    return performance


def evaluate_on_dataset(dataset, qa_pipeline):
    accuracy = 0
    total = 0
    for example in dataset:
        context, question, answers = example
        prediction = qa_pipeline({"context": context, "question": question}, truncation=True)[
            "answer"
        ]
        if prediction in answers:
            accuracy += 1
        total += 1
    print(f"The number of examples = {total}")
    print(f"The accuracy of exact matching = {100 * accuracy / total}")
    return {"accuracy": np.round(100 * accuracy / total, 1), "no_of_examples": total}
