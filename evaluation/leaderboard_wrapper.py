import sys
sys.path.append("..")
sys.path.append("../..")
import pandas as pd


from tasks.TaskTypes import TaskType
from TestRunner import OperationRuns
from evaluation.evaluation_engine import execute_model

"""This is a dict for default models to be included in the leaderboard.
Each entry is a combination of (MODEL_NAME, DATA_NAME) used in 
Huggingface: https://huggingface.co/
"""    
DEFAULT_LEADERBOARD_MODELS = {
    
    "QUESTION_ANSWERING": [
        ("deepset/roberta-base-squad2", "squad"),
        ("bert-large-uncased-whole-word-masking-finetuned-squad", "squad"),
        #("distilbert-base-cased-distilled-squad", "squad")
    ],
    "TEXT_CLASSIFICATION": [
        # sentiment analysis
        ("textattack/roberta-base-imdb", "imdb"),
    ],
    "TEXT_TAGGING": [],
    "DIALOGUE_ACT_TO_TEXT": [],
    "TABLE_TO_TEXT": [],
    "RDF_TO_TEXT": [],
    "RDF_TO_RDF": [],
    "QUESTION_GENERATION": [],
    "AMR_TO_TEXT": [],
    "E2E_TASK": [],
}


def create_leaderboard_for_task(task_type, trans_names_to_run=None, percentage_of_examples=20):
    """Given a task type, the function runs a list of perations
    and return a 

    Args:
        task_type (Literal): Task as specified in tasks.taskTypes.
        trans_names_to_run (List[str], optional): 
            Can choose to only run some of the transformations, 
            by giving a list of names for a given transformation. 
            Defaults to None.
        percentage_of_examples (int, optional): 
            The percentage of examples to perturb. 
            Defaults to 1.

    Raises:
        ValueError: [description]
    """
    if task_type not in TaskType:
        #  TODO: this might be more useful somewhere else.
        raise ValueError(f"{task_type} does not exist.")
    task_name = TaskType(task_type).name
    all_trans = list(OperationRuns.get_all_operations_for_task(task_type))
    all_trans_names = {t.name(): i for i, t in enumerate(all_trans)}
    transformations = []
    if trans_names_to_run is not None:
        for name in trans_names_to_run:
            if name in all_trans_names:
                transformations.append(all_trans[all_trans_names[name]])
            else:
                print(f"WARNING: {name} is not supported.")
    else:
        transformations = all_trans
    # filtered transformations
    print(f"""
    Creating leaderboard for task: [{task_name}].
    Transformations being run:
    \t{", ".join([t.name() for t in transformations])}
    """)
    result_dict = {t.name(): {"Transformation": t.name()} for t in transformations}
    for model_name, dataset_name in DEFAULT_LEADERBOARD_MODELS[task_name]:
        # TODO: should we try to allow passing in models, rather than model names?
        # in this leaderboard case the default implementation will cause unnecessary
        # multiple inputs.
        print(f"---- Evaluating {model_name} on {dataset_name} -----")
        for trans in transformations:
            print(f"| Transformation: {trans.name()}")
            #try:
            if True:
                result = execute_model(
                    implementation=trans.__class__,
                    task_type=task_name,
                    model_name=model_name,
                    dataset=dataset_name,
                    percentage_of_examples=percentage_of_examples)
                if "accuracy" in result:
                    key, pt_key = "accuracy", "pt_accuracy"
                if "bleu" in result:
                    key, pt_key = "bleu", "pt_bleu"
                result_dict[trans.name()][f"{model_name}\n({dataset_name})"] = result[key]-result[pt_key]
            #except:
            #    continue
    df_result = pd.DataFrame(list(result_dict.values()))
    print("Finished! The leaderboard:")
    print(df_result.to_markdown(index=False))
    filename = f"leaderboard_{TaskType(task_type).name}.csv"
    df_result.to_csv(filename)
    print("Saved the result to f{filename}")
    return result_dict
            
        
if __name__ == '__main__':
    for task_type in TaskType:
        create_leaderboard_for_task(task_type)