import torch
from sibyl import Concept2Sentence

from nlaugmenter.interfaces.SentenceOperation import SentenceAndTargetOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class C2S(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        # type of linguistic change
        "lexical",
        "semantic",
        # type of algorithm
        "model-based",
        "transformer-based",
        "api-based",
        "tokenizer-required",
        # naturalness of the generation
        "unnaturally-written",
        # potential accuracy & precision of the generation
        "possible-meaning-alteration",
        "low-precision",
        "high-coverage",
        "high-generations",
    ]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        dataset=None,
        extract="token",
        gen_beam_size=10,
        text_min_length=10,
        text_max_length=32,
        device="cpu",
        task_config=None,
    ):

        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.max_outputs = max_outputs
        self.c2s = Concept2Sentence(
            dataset=dataset,
            extract=extract,
            gen_beam_size=gen_beam_size,
            text_min_length=text_min_length,
            text_max_length=text_max_length,
            device=device,
        )
        self.task_config = task_config
        if self.task_config is None:
            self.task_config = {
                "input_idx": [1],
                "tran_type": "INV",
                "label_type": "hard",
                "task_name": "topic",
            }
        if torch.cuda.is_available():
            self.device = "cuda"

    def generate(self, sentence: str, target=None):
        """
        Generates a new sentence from the concept
        keywords extracted from the input sentence,
        optionally using the target to improve
        concept selection.


        Parameters
        ----------
        sentence : str
            the input sentence(s) from which the
            concepts will be extracted and
            transformed into new, related outputs
        target : int (optional)
            the class label of the dataset provided
            at initialization; used to provide a
            salience-guided selection of concepts
            and intended to improve semantic
            relatedness with the original sentence
        """
        new_sentences, new_targets = [], []
        for _ in range(self.max_outputs):
            new_sentence, new_target = self.c2s.transform_Xy(
                sentence, target, self.task_config
            )
            new_sentences.append(new_sentence[0])
            new_targets.append(new_target)
        return list(zip(new_sentences, new_targets))


# if __name__ == '__main__':
#     import json
#     tf = C2S(max_outputs=1)
#     test_cases = [("I hate how long loading the models takes to select better keyphrases.", 1, "sst2"),
#                   ("I really love this movie a lot!", 1, "sst2"),
#                   ("David Beckham scores 10 goals to win the game for Manchester United.", 1, "ag_news"),
#                   ("The Pentagon has released the names of the following us service members killed recently in Iraq.", 0, "ag_news"),
#                   ("America's best airline? Hawaiian Airlines is putting up impressive numbers, including some that really matter to travelers", 2, "ag_news"),]
#     results = []
#     for (sentence, target, dataset) in test_cases:
#         # uncomment to get better extracted concepts
#         # tf = C2S(max_outputs=1, dataset=dataset)
#         new_sentence, new_target = tf.generate(sentence, target)
#         results.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence, "target": target},
#             "outputs": {"new_sentence": new_sentence, "new_target": new_target}
#         })
#     json_file = {"type": tf.name(), "test_cases": results}
#     print(json.dumps(json_file, indent=2))
