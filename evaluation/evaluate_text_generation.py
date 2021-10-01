import numpy as np
from datasets import load_dataset
from transformers import pipeline
from rouge_score import rouge_scorer
from dataset import KeyValueDataset
from tasks.TaskTypes import TaskType
from typing import List, Dict


# def rouge_score_1(hypotheses, references):
#     rouge_types = ["rouge1", "rouge2", "rougeL"]
#     scorer = rouge_scorer.RougeScorer(rouge_types)
#     one_gram_scores = 0.0
#     two_gram_scores = 0.0
#     rouge_L_scores = 0.0
#     for ref, hyp in zip(references, hypotheses):
#         scores=scorer.score(ref, hyp[0])
#         one_gram_scores+=scores['rouge1'][2] # [2] for f1 score
#         two_gram_scores+=scores['rouge2'][2]
#         rouge_L_scores+=scores['rougeL'][2]
#     return one_gram_scores/len(hypotheses), two_gram_scores/len(hypotheses), rouge_L_scores/len(hypotheses)


def rouge_score(hypotheses: List[List[str]], references: List[str]) -> Dict[str, float]:
    '''Compute Rouge score between list of references and list of list of hypothesis.'''
    rouge_types = ["rouge1", "rouge2", "rougeL"]
    scorer = rouge_scorer.RougeScorer(rouge_types)
    rouge_scores = [0.0]*len(rouge_types) # list contains rouge1, rouge2, rougeL scores
    for hypothesis, reference in zip(hypotheses, references):
        all_hyp_scores = [scorer.score(reference, hyp) for hyp in hypothesis]
        for rouge_type in rouge_types:
            best_hyp_score_index = max(
                     range(len(all_hyp_scores)), key=lambda x:all_hyp_scores[x][rouge_type]
                 )
            best_hyp = all_hyp_scores[best_hyp_score_index]
            for i in range(len(rouge_scores)):
                rouge_scores[i] += best_hyp[rouge_types[i]][2]#[2] for f1 score
    return np.array(rouge_scores)/len(references)


def evaluate(
    operation, evaluate_filter, model_name, dataset_name, split="test[:20%]"
):
    # load model
    if model_name is None:
        model_name = "sshleifer/distilbart-xsum-12-6"
    # load test set
    if dataset_name is None:
        dataset_name = "xsum"

    print(
        f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model."
    )
    hf_dataset = (
        load_dataset(dataset_name, "3.0.0", split=split)
        if dataset_name == "xsum"
        else load_dataset(dataset_name, split=split)
    )

    dataset = KeyValueDataset.from_huggingface(
        hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ["document", "summary"]
    )
    summarization_pipeline = pipeline(
        "summarization", model=model_name, tokenizer=model_name
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
    print("Here is the performance of the model on the filtered set")
    filtered_dataset = dataset.apply_filter(filter, subfields=["document"])
    return performance_on_dataset(filtered_dataset, summarization_pipeline)


"""
Evaluates performance on the original set
and on the perturbed set.
"""


def transformation_performance(
    dataset, summarization_pipeline, transformation
):
    performance = performance_on_dataset(
        dataset, summarization_pipeline
    )
    pt_dataset = dataset.apply_transformation(
        transformation, subfields=["document"]
    )
    print("Here is the performance of the model on the transformed set")
    pt_performance = performance_on_dataset(
        pt_dataset, summarization_pipeline
    )
    return {"rouge1": performance["rouge1"], "pt_rouge1": pt_performance["rouge1"],
            "rouge2": performance["rouge2"], "pt_rouge2": pt_performance["rouge2"],
            "rougeL": performance["rougeL"], "pt_rougeL": pt_performance["rougeL"]}


def performance_on_dataset(dataset, summarization_pipeline):
    references = []
    raw_hypotheses = []
    print(f"Length of Evaluation dataset is {len(dataset)}")

    for example in dataset:
        article, gold_summary = example
        max_len = (
            len(gold_summary.split(" ")) + 10
        )  # approximate max length to control summary generation upto length of gold summary
        predicted_summary = summarization_pipeline(
            article, truncation=True, max_length=max_len
        )[0]["summary_text"]

        references.append(gold_summary)
        raw_hypotheses.append([predicted_summary])
    predicted_summary_scores = rouge_score(raw_hypotheses, references)

    print(f"Predicted ROUGE-1 score = {predicted_summary_scores[0]},\n"
          f"Predicted ROUGE-2 score = {predicted_summary_scores[1]},\n"
          f"Predicted ROUGE-L score = {predicted_summary_scores[2]}")
    return {
        "rouge1": np.round(predicted_summary_scores[0], 3),
        "rouge2": np.round(predicted_summary_scores[1], 3),
        "rougeL": np.round(predicted_summary_scores[2], 3)
    }


def rouge_test_case():
    """Test cases for single and multi-reference of rouge_score function."""
    reference = "I want to cancel the policy ."
    hypothesis_1 = "I need to discontinue my policy ."
    hypothesis_2 = "We canceled our policy ."

    res_1 = rouge_score([[hypothesis_1]], [reference])
    print(res_1)

    res_2 = rouge_score([[hypothesis_1], [hypothesis_2]], [reference])
    print(res_2)

"""
if __name__ == "__main__":
    rouge_test_case()
    print(rouge_score.__doc__)
"""
