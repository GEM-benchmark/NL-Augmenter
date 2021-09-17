import numpy as np
import torch.cuda
from datasets import load_dataset
from sacrebleu import corpus_bleu
from transformers import pipeline

from dataset import KeyValueDataset
from tasks.TaskTypes import TaskType


def sacrebleu_score(hypotheses, references):
    return corpus_bleu(hypotheses, [references]).score


def _process_data(dataset_name, split):
    '''Function for extracting expected columns and create a dataset.'''
    if dataset_name == "xsum":
        hf_dataset = load_dataset(dataset_name, "3.0.0", split=split)
        dataset = KeyValueDataset.from_huggingface(
            hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ["document", "summary"]
        )
        return dataset
    elif dataset_name == "cnn_dailymail":
        hf_dataset = load_dataset(dataset_name,"3.0.0", split=split)
        dataset = KeyValueDataset.from_huggingface(
            hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ["article", "highlights"]
        )
        return dataset
    elif dataset_name == "big_patent":
        hf_dataset = load_dataset(dataset_name, split)
        dataset = KeyValueDataset.from_huggingface(
            hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ["description", "abstract"]
        )
        return dataset
    elif dataset_name == "billsum":
        hf_dataset = load_dataset(dataset_name, split)
        dataset = KeyValueDataset.from_huggingface(
            hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ["text", "summary"]
        )


def evaluate(
    operation, evaluate_filter, model_name,
        dataset_name, split="test[:20%]", is_cuda=torch.cuda.is_available()):
    # load model
    if model_name is None: model_name = "sshleifer/distilbart-xsum-12-6" # default model
    # load test set
    if dataset_name is None: dataset_name = "xsum" # default dataset

    print(
        f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model."
    )
    summarization_pipeline = pipeline(
        "summarization", model=model_name, tokenizer=model_name, device=0 if is_cuda else -1)
    #percent = f"[{split.split('[')[-1]}" if "[" in split else ""
    #if dataset_name == "wikihow": split = "all[:1%]"  # f"all{percent}"

    dataset = _process_data(dataset_name, split)
    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )

    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )
    if evaluate_filter:
        performance = filter_performance(
            dataset, summarization_pipeline, filter=operation
        )
    else:
        performance = transformation_performance(
            dataset, summarization_pipeline, transformation=operation
        )

    performance["model_name"] = model_name
    performance["split"] = split
    performance["dataset_name"] = dataset_name
    return performance


def filter_performance(dataset, summarization_pipeline, filter):
    '''Evaluate performance on filtered dataset.'''
    print("Here is the performance of the model on the filtered set")
    filtered_dataset = dataset.apply_filter(filter, subfields=["document"])
    return performance_on_dataset(filtered_dataset, summarization_pipeline)


def transformation_performance(
    dataset, summarization_pipeline, transformation
):
    '''Evaluates performance on the original set and on the perturbed set.'''
    performance = performance_on_dataset(
        dataset, summarization_pipeline
    )  # 15.989 BLEU
    pt_dataset = dataset.apply_transformation(
        transformation, subfields=["document"]
    )
    print("Here is the performance of the model on the transformed set")
    pt_performance = performance_on_dataset(
        pt_dataset, summarization_pipeline
    )  # 11.830 BLEU
    return {"bleu": performance["bleu"], "pt_bleu": pt_performance["bleu"]}


def performance_on_dataset(dataset, summarization_pipeline):
    '''Evaluate performance on a given dataset.'''
    references = []
    raw_hypotheses = []
    print(f"Length of Evaluation dataset is {len(dataset)}")

    for i,example in enumerate(dataset):
        print(i)
        article, gold_summary = example
        max_len = (
            len(gold_summary.split(" ")) + 10
        )  # approximate max length to control summary generation upto length of gold summary
        predicted_summary = summarization_pipeline(
            article, truncation=True, max_length=max_len
        )[0]["summary_text"]

        references.append(gold_summary)
        raw_hypotheses.append(predicted_summary)
    predicted_summary_score = sacrebleu_score(
        raw_hypotheses, references
    )  # 15.989 BLEU

    print(f"Predicted BLEU score = {predicted_summary_score}")
    return {
        "bleu": np.round(predicted_summary_score, 1),
    }
