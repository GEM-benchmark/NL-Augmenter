from tasks.TaskTypes import TaskType
import numpy as np
import enum

from datasets import load_dataset
from transformers import pipeline

from dataset import TextLineDataset, KeyValueDataset
import torch
# make this to work for three task.

class SENTIMENT_LABELS(enum.Enum):
    NEGATIVE = 0
    POSITIVE = 1
class NLI_LABELS(enum.Enum):
    ENTAILMENT = 0
    NEUTRAL = 1
    CONTRADICTION = 2
class QQP_LABEL(enum.Enum):
    NON_DUPLICATE = 0
    DUPLICATE = 1


def _process_data(dataset_name, split):
    if dataset_name in ["qqp", "sst2"]:
        hf_dataset = load_dataset("glue", dataset_name, split=split)
    elif dataset_name in ['clue']:
        hf_dataset = load_dataset(dataset_name, "cluewsc2020", split=split)
    else:
        hf_dataset = load_dataset(dataset_name, split=split)

    if dataset_name == "imdb":
        label_name = "label"
        label_func = lambda x: SENTIMENT_LABELS.POSITIVE if x == 1 else SENTIMENT_LABELS.NEGATIVE
        instance_name = ["text"]
        data_class = TextLineDataset
    elif dataset_name == "sst2":
        label_name = "label"
        label_func = lambda x: SENTIMENT_LABELS.POSITIVE if x == 1 else SENTIMENT_LABELS.NEGATIVE
        instance_name = ["sentence"]
        data_class = TextLineDataset
    elif dataset_name == "clue":
        label_name = "label"
        label_func = lambda x: SENTIMENT_LABELS.POSITIVE if x == 1 else SENTIMENT_LABELS.NEGATIVE
        instance_name = ["text"]
        data_class = TextLineDataset
    elif dataset_name in ["multi_nli", "snli"]:
        label_name = "label"
        def label_func(d):
            if d == 0: return NLI_LABELS.ENTAILMENT
            elif d == 1: return NLI_LABELS.NEUTRAL
            elif d == 2: return NLI_LABELS.CONTRADICTION
        instance_name = ["premise","hypothesis"]
        data_class = KeyValueDataset
    elif dataset_name == "qqp":
        label_name = "label" 
        instance_name = ["question1", "question2"]
        def label_func(d):
            if d == 1: return QQP_LABEL.DUPLICATE
            else: return QQP_LABEL.NON_DUPLICATE
        data_class = KeyValueDataset
    datasets = data_class.from_huggingface(
        hf_dataset, fields=instance_name+[label_name], 
        task_type=TaskType.TEXT_CLASSIFICATION, max_size=1000)
    return datasets, label_func

def _get_instance_by_keys(example):
    if type(example) == str: return example
    elif len(example) == 1: return example[0] if type(example[0]) == str else example[0][0]
    else:return tuple([e if type(e) == str else e[0] for e in example])

def _process_model_pred(model_name, pred):
    if model_name == "aychang/roberta-base-imdb":
        return SENTIMENT_LABELS.POSITIVE if pred =="pos" else SENTIMENT_LABELS.NEGATIVE
    elif model_name in [
        "textattack/roberta-base-imdb",
        "textattack/roberta-base-SST-2",
        "clue/roberta_chinese_base",
        "clue/roberta_chinese_clue_large"]:
        return SENTIMENT_LABELS.POSITIVE if pred == "LABEL_1" else SENTIMENT_LABELS.NEGATIVE
    elif model_name in [
        "ji-xin/roberta_base-QQP-two_stage",
        "textattack/bert-base-uncased-QQP"]:
        return QQP_LABEL.DUPLICATE if pred == "LABEL_1" else QQP_LABEL.NON_DUPLICATE
    elif model_name == "roberta-large-mnli":
        if pred == "CONTRADICTION": return NLI_LABELS.CONTRADICTION
        elif pred == "ENTAILMENT": return NLI_LABELS.ENTAILMENT
        else: return NLI_LABELS.NEUTRAL
    elif model_name == "textattack/bert-base-uncased-snli":
        if pred == "LABEL_0": return NLI_LABELS.CONTRADICTION
        elif pred == "LABEL_1": return NLI_LABELS.ENTAILMENT
        else: return NLI_LABELS.NEUTRAL
    

def evaluate(
    operation, evaluate_filter, model_name, 
    dataset_name, split="test[:20%]", batch_size=8, is_cuda=torch.cuda.is_available()):
    if model_name is None: model_name = "aychang/roberta-base-imdb"
    if dataset_name is None: dataset_name = "imdb"
    print(f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model.")

    # For the roberta_chinese_base model, you have to call the tokenizer for BERT instead:
    # https://huggingface.co/clue/roberta_chinese_base
    if model_name in [
        "clue/roberta_chinese_base",
        "clue/roberta_chinese_clue_large"]:
        text_classification_pipeline = pipeline(
            "sentiment-analysis", model=model_name, tokenizer="bert-base-chinese",
            device=0 if is_cuda else -1)
    else:
        text_classification_pipeline = pipeline(
            "sentiment-analysis", model=model_name, tokenizer=model_name,
            device=0 if is_cuda else -1)
    
    percent = f"[{split.split('[')[-1]}" if "[" in split else ""
    if dataset_name == "multi_nli": split = f"validation_matched{percent}"
    elif dataset_name != "imdb": split = f"validation{percent}"
    
    performance = {
        "model_name": model_name,
        "split": split,
        "dataset_name": dataset_name,
    }
    dataset, label_func = _process_data(dataset_name, split)

    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset")
    if evaluate_filter:
        filtered_dataset = dataset.apply_filter(operation)
        print("Here is the performance of the model on the filtered set")
        accuracy, total = evaluate_dataset(
            text_classification_pipeline, filtered_dataset, 
            model_name, label_func, batch_size=batch_size)
        performance["accuracy"] = accuracy
        performance["no_of_examples"] = total
    else:
        accuracy, total = evaluate_dataset(
            text_classification_pipeline, dataset, 
            model_name, label_func, batch_size=batch_size)
        performance["accuracy"] = accuracy
        performance["no_of_examples"] = total
        pt_dataset = dataset.apply_transformation(operation)
        if pt_dataset is None:
            print(f"No transformation applied.")
            accuracy = 0
        else:
            print("Here is the performance of the model on the transformed set")
            accuracy, _ = evaluate_dataset(
                text_classification_pipeline, pt_dataset, 
                model_name, label_func, batch_size=batch_size)
        performance["pt_accuracy"] = accuracy
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    return performance

def _get_model_pred(model, examples, batch_size):
    all_preds = []
    with torch.no_grad():
        for e in (range(0, len(examples), batch_size)):

            all_preds += model(examples[e:e+batch_size], truncation=True)
    return [a["label"] for a in all_preds]

def evaluate_dataset(
    text_classification_pipeline, dataset, model_name, label_func, batch_size=32):
    accuracy = 0
    total = 0
    examples = [_get_instance_by_keys(list(raw_text)[:-1]) for raw_text in dataset]
    labels = [label_func(list(raw_text)[-1]) for raw_text in dataset]
    raw_preds = _get_model_pred(text_classification_pipeline, examples, batch_size=batch_size)
    preds = [_process_model_pred(model_name, raw_pred) for raw_pred in raw_preds]
    total = len(labels)
    accuracy = 0
    if total != 0:
        accuracy = np.round(100 * np.mean(np.array(labels) == np.array(preds)))
    print(f"The accuracy on this subset which has {total} examples = {accuracy}")
    return accuracy, total
