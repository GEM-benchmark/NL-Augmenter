from datasets import load_dataset
from transformers import pipeline
from sacrebleu import sentence_bleu
from seqeval.metrics import accuracy_score

from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation
from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType

"""
This is the evaluation engine.
Currently has been implemented for SentenceTransformation:
eg. python evaluate.py -t butter_fingers_perturbation
"""


def evaluate(
    implementation,
    task_type,
    locale="en",
    model=None,
    dataset=None,
    percent_of_examples=None,
):
    # The evaluation engine would effectively do the following
    # (1) Loading a standard model and a test set (the model's original test set would be the best choice)
    # (2) Executing perturbations to generate the perturbed test set.
    # (3) Executing these against the model and evaluate its performance (display nicely :P )
    # (4) Writing a neat README.
    task_type = get_task_type(implementation, task_type)
    execute_model(
        implementation, task_type, locale, model, dataset, percent_of_examples
    )
    return


def get_task_type(implementation, task_type):
    if task_type is None:
        print(
            "Undefined task type, switching to default task %s",
            implementation.tasks[0].name,
        )
        return str(implementation.tasks[0]).split(".")[1]
    return task_type


def execute_model(
    implementation,
    task_type,
    locale="en",
    model=None,
    dataset=None,
    percentage_of_examples=20,
):
    interface = implementation.__bases__[0]  # SentenceTransformation
    impl = implementation()
    if locale is "en":
        if (
            isinstance(impl, SentenceOperation)
            and TaskType[task_type] == TaskType.TEXT_CLASSIFICATION
        ):
            evaluate_text_classifier(
                impl, model, dataset, split=f"test[:{percentage_of_examples}%]"
            )
        elif (
            isinstance(impl, QuestionAnswerOperation)
            and TaskType[task_type] == TaskType.QUESTION_ANSWERING
        ):
            evaluate_question_answering_model(
                impl, model, dataset, split=f"validation[:{percentage_of_examples}%]"
            )
        elif (
            isinstance(impl, SentenceOperation)
            and TaskType[task_type] == TaskType.TEXT_TO_TEXT_GENERATION
        ):
            evaluate_text_summarization(
                impl, model, dataset, split=f"test[:{percentage_of_examples}%]"
            )
        elif (
            isinstance(impl, TaggingOperation)
            and TaskType[task_type] == TaskType.TEXT_TAGGING
        ):
            evaluate_ner_tagging(impl, model, dataset, split=f'test[:{percentage_of_examples}%]')
        # Other if else cases should be added here.
        else:
            print(
                f"No default evaluation model exists for the interface {interface} in the locale {locale}."
                f"It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate "
                f"your perturbation on a task and a dataset, "
                f"the right place to do it would to add a new function in evaluate/evaluation_engine.py "
                f"and call it from execute_model. That's it!"
            )
    else:
        print(
            f"No default evaluation model exists in the locale {locale}."
            f"It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate "
            f"your perturbation on a task and a dataset, "
            f"the right place to do it would to add a new function in evaluate/evaluation_engine.py "
            f"and call it from execute_model. That's it!"
        )


def convert_ner_ids_to_tags(ner_tags):
    # convert list of ner ids [0,1,2,0] to list of ner tags ['0', 'B-PER', 'I-PER', '0']
    ner_tag_sequence = []
    ner_tag_dict = {1: 'B-PER', 2: 'I-PER', 3: 'B-ORG', 4: 'I-ORG', 5: 'B-LOC', 6: 'I-LOC', 7: 'B-MISC', 8: 'I-MISC'}
    for tag in ner_tags:
        if(tag in ner_tag_dict.keys()):
            ner_tag_sequence.append(ner_tag_dict[tag])
        else:
            ner_tag_sequence.append('0') # O(big O), tag for no ner token
    return ner_tag_sequence

def calculate_seq_evaluation_score(gold, prediction):
    return accuracy_score([gold], [prediction])

def create_prediction_seq(prediction, expected_seq_length):
    # create model output into ner tag sequence
    # input : model output in the form [[], [{}], [{}], []]
    # output : ['0', 'B-PER', 'I-PER', '0']
    if (prediction == []):  # corner case where model prediction is [] and gold label is not []. ex: example["tokens"] = [',']
        return ['0'] * expected_seq_length
    seq = []
    tag = ""
    for item in prediction:
        if(len(item)==0):
            seq.append('0')
        else:
            if(isinstance(item, list)):
                tag = item[0]['entity']
            elif(isinstance(item, dict)): # to handle a corner case
                tag = item['entity']
            seq.append(tag)
    return seq

def evaluate_ner_tagging(transformation, model_name, dataset_name, split='validation[:20%]'):
    # load modal
    if model_name is None:
        model_name = "dslim/bert-base-NER"
    # load test set
    if(dataset_name is None):
        dataset_name = "conll2003"

    print(f"Loading <%s> dataset to train <%s> model", dataset_name, model_name)
    dataset = load_dataset(dataset_name, split=split) if dataset_name is "conll2003" \
        else load_dataset(dataset_name, split=split)
    tagging_pipeline = pipeline("ner", model=model_name, tokenizer=model_name)

    average_score = 0.0
    average_pertubed_score = 0.0
    print(f"Length of Evaluation dataset is {len(dataset)}")
    for example in dataset:
        # Calculating the performance on the original set
        gold_tag_seq = convert_ner_ids_to_tags(example['ner_tags'])
        prediction = tagging_pipeline(example['tokens'])
        predicted_tag_seq = create_prediction_seq(prediction, len(gold_tag_seq))
        score = calculate_seq_evaluation_score(gold_tag_seq, predicted_tag_seq)
        average_score +=score

        # Calculating the performance on the perturbed set
        trans_input, trans_gold_tag_seq = transformation.generate(example['tokens'], gold_tag_seq)
        trans_gold_tag_seq = convert_ner_ids_to_tags(trans_gold_tag_seq)
        transformed_input_prediction = tagging_pipeline(trans_input)
        trans_predicted_tag_seq = create_prediction_seq(transformed_input_prediction, len(trans_gold_tag_seq))
        pt_score = calculate_seq_evaluation_score(trans_gold_tag_seq, trans_predicted_tag_seq)
        average_pertubed_score += pt_score

    average_score = average_score / len(dataset)
    average_pertubed_score = average_pertubed_score / len(dataset)

    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset} dataset")
    print(f"The average accuracy on a subset of {dataset_name} = {average_score}")
    print(f"The average accuracy on its pertubed set = {average_pertubed_score}")

def sacrebleu_score(reference, hypothesis):
    return sentence_bleu(hypothesis, [reference]).score

def evaluate_text_summarization(
    transformation, model_name, dataset_name, split="test[:20%]"
):
    # load model
    if model_name is None:
        model_name = "sshleifer/distilbart-xsum-12-6"
    # load test set
    if dataset_name is None:
        dataset_name = "xsum"

    print("Loading <%s> dataset to train <%s> model", dataset_name, model_name)
    dataset = (
        load_dataset(dataset_name, "3.0.0", split=split)
        if dataset_name is "xsum"
        else load_dataset(dataset_name, split=split)
    )

    summarization_pipeline = pipeline(
        "summarization", model=model_name, tokenizer=model_name
    )
    predicted_summary_score = 0.0
    transformed_summary_score = 0.0
    print(f"Length of Evaluation dataset is {len(dataset)}")
    for example in dataset:
        article = example["document"]
        gold_summary = example["summary"]
        max_len = (
            len(gold_summary.split(" ")) + 10
        )  # approximate max length to control summary generation upto length of gold summary
        predicted_summary = summarization_pipeline(
            article, truncation=True, max_length=max_len
        )[0]["summary_text"]
        score_list = sacrebleu_score(
            reference=gold_summary, hypothesis=predicted_summary
        )
        predicted_summary_score += score_list

        # Calculating the performance on the perturbed set
        transformed_article = transformation.generate(article)
        transformed_article_summary = summarization_pipeline(
            transformed_article, truncation=True, max_length=max_len
        )[0]["summary_text"]
        trans_score_list = sacrebleu_score(
            reference=gold_summary, hypothesis=transformed_article_summary
        )
        transformed_summary_score += trans_score_list

    predicted_summary_score = predicted_summary_score / len(dataset)
    transformed_summary_score = transformed_summary_score / len(dataset)

    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )
    print(
        f"The average bleu score on a subset of {dataset_name} = {predicted_summary_score}"
    )
    print(f"The average bleu score on its perturbed set = {transformed_summary_score}")


def evaluate_text_classifier(
    transformation, model_name, dataset_name, split="test[:20%]"
):
    # (1) load model
    if model_name is None:
        model_name = "aychang/roberta-base-imdb"
    # (2) load test set
    if dataset_name is None:
        dataset_name = "imdb"
    print("Loading <%s> dataset to train <%s> model", dataset_name, model_name)
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
    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )
    print(f"The accuracy on a subset of {dataset_name} = {100 * accuracy / total}")
    print(
        f"The accuracy on its perturbed set generated from = {100 * pt_accuracy / total}"
    )


def evaluate_question_answering_model(
    transformation, model_name, dataset_name, split="validation[:20%]"
):
    # (1) load model
    if model_name is None:
        model_name = "mrm8488/bert-tiny-5-finetuned-squadv2"
    # (2) load test set
    if dataset_name is None:
        dataset_name = "squad"
    print("Loading <%s> dataset to train <%s> model", dataset_name, model_name)
    dataset = load_dataset(dataset_name, split=split)
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    accuracy = 0
    pt_accuracy = 0
    total = 0
    for example in dataset:
        context = example["context"]
        question = example["question"]
        answers = example["answers"]["text"]
        pred = nlp({"context": context, "question": question}, truncation=True)[
            "answer"
        ]
        if pred in answers:
            accuracy += 1
        context_t, question_t, answers_t = transformation.generate(
            context, question, answers
        )
        pt_pred = nlp({"context": context_t, "question": question_t}, truncation=True)[
            "answer"
        ]
        if pt_pred in answers_t:
            pt_accuracy += 1
        total += 1
    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )
    print(f"The accuracy on a subset of {dataset_name} = {100 * accuracy / total}")
    print(
        f"The accuracy on its perturbed set generated from = {100 * pt_accuracy / total}"
    )
