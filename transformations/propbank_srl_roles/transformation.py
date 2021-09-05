from allennlp.predictors.predictor import Predictor

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.propbank_srl_roles.findargs import perturb_text


def srl_args(predictor, text, max_outputs=1):

    x = predictor.predict(sentence=text)

    verbs_list = x["verbs"]
    perturbed_texts = []

    for i in verbs_list:
        desc = i["description"]
        perturbed_texts += perturb_text(text, desc)

    if len(perturbed_texts) > max_outputs:
        perturbed_texts = perturbed_texts[:max_outputs]

    if len(perturbed_texts) == 0:
        perturbed_texts.append(text)

    return perturbed_texts


class CheckSrl(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = ["word-order", "rule-based", "external-knowledge-based", "high-precision",]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.predictor = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"
        )

    def generate(self, sentence: str):
        perturbed_texts = srl_args(
            self.predictor,
            text=sentence,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == "__main__":
    import json

    from TestRunner import convert_to_snake_case

    tf = CheckSrl(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in [
        "Andrew finally returned the French book to Chris that I bought last week",
        "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
        "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
        "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
        "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
    ]:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {
        "type": convert_to_snake_case(tf.name()),
        "test_cases": test_cases,
    }
    print(json.dumps(json_file))
"""