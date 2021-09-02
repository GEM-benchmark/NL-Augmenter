import itertools
import random

# from interfaces.SentenceOperation import SentenceAndTargetOperation
# from tasks.TaskTypes import TaskType

from sibyl import Concept2Sentence

import enum


class TaskType(enum.Enum):
    TEXT_CLASSIFICATION = (
        1,
    )  # This would include all - sentiment, emotion, etc.
    TEXT_TO_TEXT_GENERATION = (2,)
    TEXT_TAGGING = (
        3,
    )  # This would require the inputs to be in ConnLL like format
    DIALOGUE_ACT_TO_TEXT = (4,)
    TABLE_TO_TEXT = (5,)
    RDF_TO_TEXT = (6,)
    RDF_TO_RDF = (7,)
    QUESTION_ANSWERING = (8,)
    QUESTION_GENERATION = (9,)
    AMR_TO_TEXT = (10,)
    E2E_TASK = (11,)
    SENTIMENT_ANALYSIS = (
        12,
    )  # This is a specific type of text classification with unique properties
    PARAPHRASE_DETECTION = (13,)
    TEXTUAL_ENTAILMENT = (14,)
    QUALITY_ESTIMATION = (15,)

from typing import Tuple, List
"""Generic operation class. """


class Operation(object):
    languages = None
    tasks = None
    seed = 0
    heavy = False
    max_outputs = 1

    def __init__(self, seed=0, verbose=False, max_outputs=1):
        self.seed = seed
        self.verbose = verbose
        self.max_outputs = max_outputs
        if self.verbose:
            print(f"Loading Operation {self.name()}")
            
    @classmethod
    def compare(self, raw: object, pt: List[object]) -> Tuple[int, int]:
        successful_pt = 0
        failed_pt = 0
        for pt_example in pt:
            if pt_example == raw:
                failed_pt += 1
            else:
                successful_pt += 1
        return successful_pt, failed_pt

    @classmethod
    def is_heavy(cls):
        return cls.heavy

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages

    @classmethod
    def name(cls):
        return cls.__name__

class SentenceAndTargetOperation(Operation):
    """
    The base class for implementing sentence-pair-level perturbations and transformations. The target could be
    either a class label (eg. sentiment analysis) or a target utterance (eg. machine translation).

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages", "tgt_languages :: The locales and/or languages for which this perturbation is applicable. eg. "es",
    "mr","en_IN"
    """

    languages = None
    tgt_languages = None
    tasks = None

    @classmethod
    def domain(cls):
        return cls.tasks, cls.languages, cls.tgt_languages

    def generate(self, sentence: str, target: str) -> List[Tuple[str, str]]:
        raise NotImplementedError

    def filter(self, sentence: str, target: str) -> bool:
        raise NotImplementedError


class C2S(SentenceAndTargetOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]

    def __init__(self, 
                 seed=0, 
                 max_outputs=1, 
                 dataset=None, 
                 extract="token",
                 gen_beam_size=10,
                 text_min_length=10,
                 text_max_length=32,
                 device='cpu',
                 task_config=None):

        super().__init__(seed, max_outputs=max_outputs)

        self.c2s = Concept2Sentence(
                        dataset = dataset,
                        extract = extract,
                        gen_beam_size = gen_beam_size,
                        text_min_length = text_min_length,
                        text_max_length = text_max_length,
                        device = device)
        self.task_config = task_config
        if self.task_config is None:
            self.task_config = {
                'input_idx': [1],
                'tran_type': 'INV',
                'label_type': 'hard',
                'task_name': 'topic'
            }

    def generate(self, sentence: str, target: int):
        new_sentence, new_target = self.c2s.transform_Xy(sentence, target, self.task_config)
        return new_sentence[0], new_target


if __name__ == '__main__':
    import json
    tf = C2S(max_outputs=1)
    test_cases = [("I hate how long loading the models takes to select better keyphrases.", 1, "sst2"),
                  ("I really love this movie a lot!", 1, "sst2"),
                  ("David Beckham scores 10 goals to win the game for Manchester United.", 1, "ag_news"),
                  ("The Pentagon has released the names of the following us service members killed recently in Iraq.", 0, "ag_news"),
                  ("America's best airline? Hawaiian Airlines is putting up impressive numbers, including some that really matter to travelers", 2, "ag_news"),]
    results = []
    for (sentence, target, dataset) in test_cases:
        # uncomment to get better extracted concepts
        # tf = C2S(max_outputs=1, dataset=dataset)
        new_sentence, new_target = tf.generate(sentence, target)
        results.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target}, 
            "outputs": {"new_sentence": new_sentence, "new_target": new_target}
        })
    json_file = {"type": tf.name(), "test_cases": results}
    print(json.dumps(json_file, indent=2))

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = ButterFingersPerturbation(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))
"""
