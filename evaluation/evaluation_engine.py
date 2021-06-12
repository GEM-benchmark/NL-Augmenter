from datasets import load_dataset
from transformers import pipeline
import sacrebleu

from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from dataset import TextLineDataset, KeyValueDataset

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


def sacrebleu_score(hypotheses, references):
    return sacrebleu.corpus_bleu(hypotheses, [references]).score


def evaluate_text_summarization(
    transformation, model_name, dataset_name, split="test[:20%]"
):
    if model_name is None:
        model_name = "sshleifer/distilbart-xsum-12-6"
    if dataset_name is None:
        dataset_name = "xsum"

    print("Loading <%s> dataset to train <%s> model", dataset_name, model_name)
    hf_dataset = (
        load_dataset(dataset_name, "3.0.0", split=split)
        if dataset_name is "xsum"
        else load_dataset(dataset_name, split=split)
    )

    dataset = KeyValueDataset.from_huggingface(
        hf_dataset, TaskType.TEXT_TO_TEXT_GENERATION, ['document', 'summary'])
    pt_dataset = dataset.apply_transformation(transformation, subfields=['document'])

    summarization_pipeline = pipeline(
        "summarization", model=model_name, tokenizer=model_name
    )
    predicted_summary_score = 0.0
    transformed_summary_score = 0.0
    
    references = []
    raw_hypotheses = []
    pt_hypotheses = []

    for raw_example, pt_example in zip(dataset, pt_dataset):
        article, gold_summary = raw_example
        transformed_article, _ = pt_example

        max_len = (
            len(gold_summary.split(" ")) + 10
        )  # approximate max length to control summary generation upto length of gold summary
        predicted_summary = summarization_pipeline(
            article, truncation=True, max_length=max_len
        )[0]["summary_text"]
        
        transformed_article_summary = summarization_pipeline(
            transformed_article, truncation=True, max_length=max_len
        )[0]["summary_text"]
        
        references.append(gold_summary)
        raw_hypotheses.append(predicted_summary)
        pt_hypotheses.append(transformed_article_summary)
        
    predicted_summary_score = sacrebleu_score(raw_hypotheses, references) # 15.989 BLEU
    transformed_summary_score = sacrebleu_score(pt_hypotheses, references) # 11.830 BLEU

    print(
        f"Here is the performance of the model {model_name} on the {split} split of the {dataset_name} dataset"
    )
    print(
        f"The bleu score on a subset of {dataset_name} = {predicted_summary_score}"
    )
    print(f"The bleu score on its perturbed set = {transformed_summary_score}")


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
    hf_dataset = load_dataset(dataset_name, split=split)
    
    dataset = TextLineDataset.from_huggingface(hf_dataset, ['text', 'label'])
    pt_dataset = dataset.apply_transformation(transformation)
    
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    nlp = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
    accuracy = 0
    pt_accuracy = 0
    total = 0
    for raw_example, pt_example in zip(dataset, pt_dataset):
        raw_text, label = raw_example
        pt_text, _ = pt_example
       
        pred = nlp(raw_text, truncation=True)[0]["label"]
        if (pred == "pos" and label == 1) or (pred == "neg" and label == 0):
            accuracy += 1
        
        pt_pred = nlp(pt_text, truncation=True)[0]["label"]
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
    hf_dataset = load_dataset(dataset_name, split=split)
    dataset = KeyValueDataset.from_huggingface(
        hf_dataset, TaskType.QUESTION_ANSWERING, ['context', 'question', 'answers'])
    pt_dataset = dataset.apply_transformation(transformation)
    
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    accuracy = 0
    pt_accuracy = 0
    total = 0
    for raw_example, pt_example in zip(dataset, pt_dataset):
        context, question, answers = raw_example
        context_t, question_t, answers_t = pt_example

        pred = nlp({"context": context, "question": question}, truncation=True)[
            "answer"
        ]
        if pred in answers:
            accuracy += 1
        
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
