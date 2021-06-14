from datasets import load_dataset
from transformers import pipeline
from sacrebleu import corpus_bleu
import numpy as np
from seqeval.metrics import accuracy_score


def sacrebleu_score(hypotheses, references):
    return corpus_bleu(hypotheses, [references]).score


def convert_ner_ids_to_tags(ner_tags):
    # convert list of ner ids [0,1,2,0] to list of ner tags ['0', 'B-PER', 'I-PER', '0']
    ner_tag_sequence = []
    ner_tag_dict = {1: 'B-PER', 2: 'I-PER', 3: 'B-ORG', 4: 'I-ORG', 5: 'B-LOC', 6: 'I-LOC', 7: 'B-MISC', 8: 'I-MISC'}
    for tag in ner_tags:
        ner_tag_sequence.append(ner_tag_dict.get(tag, "0"))  # '0', tag for no ner token
    return ner_tag_sequence


def create_prediction_seq(prediction, expected_seq_length):
    # create model output into ner tag sequence
    # input : model output in the form [[], [{ner-info}], [{ner-info}], []]
    # output : ['0', 'B-PER', 'I-PER', '0']
    if (
            prediction == []):  # corner case where model prediction is [] and gold label is not []. ex: example["tokens"] = [',']
        return ['0'] * expected_seq_length
    seq = []
    tag = ""
    for item in prediction:
        if (len(item) == 0):
            seq.append('0')
        else:
            if (isinstance(item, list)):
                tag = item[0]['entity']
            elif (isinstance(item, dict)):  # to handle a corner case
                tag = item['entity']
            seq.append(tag)
    return seq


def evaluate_ner_tagging(operation, model_name, dataset_name, split='validation[:20%]', evaluate_filter=False):
    # load modal
    if model_name is None:
        model_name = "dslim/bert-base-NER"
    # load test set
    if dataset_name is None:
        dataset_name = "conll2003"

    print(f"Loading <{dataset_name}> dataset to evaluate <{model_name}> model.")
    dataset = load_dataset(dataset_name, split=split)
    tagging_pipeline = pipeline("ner", model=model_name, tokenizer=model_name)

    average_score = 0.0
    average_pertubed_score = 0.0
    print(f"Length of Evaluation dataset is {len(dataset)}")
    if evaluate_filter:
        filter_true_average_score = 0.0
        filter_false_average_score = 0.0
        filter_true_count = 0  # This will track the number of examples where the filter is +ve
        filter_false_count = 0  # This will track the number of examples where the filter is -ve
    for example in dataset:
        # Calculating the performance on the original set
        gold_tag_seq = convert_ner_ids_to_tags(example['ner_tags'])
        prediction = tagging_pipeline(example['tokens'])
        predicted_tag_seq = create_prediction_seq(prediction, len(gold_tag_seq))
        score = accuracy_score([gold_tag_seq], [predicted_tag_seq])
        average_score += score
        if evaluate_filter:
            # The Operation is a "filter"
            if operation.filter(example['tokens'], gold_tag_seq):
                filter_true_average_score += score
                filter_true_count += 1
            else:
                filter_false_average_score += score
                filter_false_count += 1
        else:
            # The Operation is a "transformation"
            # Calculating the performance on the perturbed set
            trans_input, trans_gold_tag_seq = operation.generate(example['tokens'], gold_tag_seq)
            trans_gold_tag_seq = convert_ner_ids_to_tags(trans_gold_tag_seq)
            transformed_input_prediction = tagging_pipeline(trans_input)
            trans_predicted_tag_seq = create_prediction_seq(transformed_input_prediction, len(trans_gold_tag_seq))
            pt_score = accuracy_score([trans_gold_tag_seq], [trans_predicted_tag_seq])
            average_pertubed_score += pt_score

    average_score = average_score / len(dataset) * 100

    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset} dataset")
    print(f"The average accuracy on a subset of {dataset_name} = {average_score}")
    performance = {
        "model_name": model_name,
        "split": split,
        "dataset_name": dataset_name,
        "accuracy": np.round(average_score, 1),
    }
    if evaluate_filter:
        filter_true_average_score = filter_true_average_score / filter_true_count * 100
        filter_false_average_score = filter_false_average_score / filter_false_count * 100
        print(
            f"The average accuracy of {filter_true_count} examples which pass the filter = {filter_true_average_score}")
        print(
            f"The average accuracy of {filter_false_count} examples which fail the filter = {filter_false_average_score}")
        performance["filter_true_count"] = filter_true_count
        performance["filter_false_count"] = filter_false_count
        performance["filter_true_average_score"] = filter_true_average_score
        performance["filter_false_average_score"] = filter_false_average_score
    else:
        performance["pt_accuracy"]: np.round(average_pertubed_score, 1)
        average_pertubed_score = average_pertubed_score / len(dataset) * 100
        print(f"The average accuracy on its perturbed set = {average_pertubed_score}")

    return performance
