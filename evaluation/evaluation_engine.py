from datasets import load_dataset
from transformers import pipeline

"""
This is the evaluation engine.
Currently has been implemented for SentenceTransformation:
eg. python evaluate.py -t butter_fingers_perturbation
"""


def evaluate(implementation, locale, model, dataset, percent_of_examples):
    # The evaluation engine would effectively do the following
    # (1) Loading a standard model and a test set (the model's original test set would be the best choice)
    # (2) Executing perturbations to generate the perturbed test set.
    # (3) Executing these against the model and evaluate its performance (display nicely :P )
    # (4) Writing a neat README.
    interface = implementation.__bases__[0]  # SentenceTransformation
    impl = implementation()
    execute_model(impl, interface, locale, model, dataset, percent_of_examples)
    return


def evaluate_text_classifier(transformation, model_name, dataset_name,
                             split='test[:20%]'):
    # (1) load model
    if model_name is None:
        model_name = "aychang/roberta-base-imdb"
    # (2) load test set
    if dataset_name is None:
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
    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset} dataset")
    print(f"The accuracy on a subset of {dataset_name} = {100 * accuracy / total}")
    print(f"The accuracy on its perturbed set generated from = {100 * pt_accuracy / total}")


def evaluate_question_answering_model(transformation, model_name,
                                      dataset_name, split='validation[:20%]'):
    # (1) load model
    if model_name is None:
        model_name = "mrm8488/bert-tiny-5-finetuned-squadv2"
    # (2) load test set
    if dataset_name is None:
        dataset_name = 'squad'
    dataset = load_dataset(dataset_name, split=split)
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    # (3) Execute perturbation
    # (4) Execute the performance of the original set and the perturbed set
    accuracy = 0
    pt_accuracy = 0
    total = 0
    for example in dataset:
        context = example["context"]
        question = example["question"]
        answers = example["answers"]["text"]
        pred = nlp({"context": context, "question": question}, truncation=True)["answer"]
        if pred in answers:
            accuracy += 1
        context_t, question_t, answers_t = transformation.generate(context, question, answers)
        pt_pred = nlp({"context": context_t, "question": question_t}, truncation=True)["answer"]
        if pt_pred in answers_t:
            pt_accuracy += 1
        total += 1
    print(f"Here is the performance of the model {model_name} on the {split} split of the {dataset} dataset")
    print(f"The accuracy on a subset of {dataset_name} = {100 * accuracy / total}")
    print(f"The accuracy on its perturbed set generated from = {100 * pt_accuracy / total}")


def execute_model(impl, interface, locale, model=None, dataset=None, percentage_of_examples=20):
    if interface.__name__ is "SentenceTransformation" and locale is "en":
        evaluate_text_classifier(impl, model, dataset, split=f'test[:{percentage_of_examples}%]')
    elif interface.__name__ is "QuestionAnswerTransformation" and locale is "en":
        evaluate_question_answering_model(impl, model, dataset, split=f'validation[:{percentage_of_examples}%]')
    # Other if else cases should be added here.
    else:
        print(f"No default evaluation model exists for the interface {interface} in the locale {locale}."
              f"It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate "
              f"your perturbation on a task and a dataset, "
              f"the right place to do it would to add a new function in evaluate/evaluation_engine.py "
              f"and call it from execute_model. That's it!")
