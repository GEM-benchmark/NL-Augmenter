from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType
from transformations.decontextualize_sentence.decontextualizer import decontextualize_text


class Decontextualize(SentencePairOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
        TaskType.TEXTUAL_ENTAILMENT
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=3):
        """
        :param seed: Set to 0 for reproducibility
        :param max_outputs: Cap on max number of decontextualize sentences
        """
        super().__init__(seed, max_outputs=max_outputs)
        from allennlp.predictors.predictor import Predictor
        self.predictor = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"
        )

    def generate(self, sentence1: str, sentence2: str, target: str):

        srl = self.predictor.predict(sentence=sentence2)

        verbs_list = srl["verbs"]
        decon_texts = []

        for verb in verbs_list:
            general_sen = decontextualize_text(verb, srl["words"])
            if general_sen not in decon_texts:
                if general_sen != " ".join(srl["words"]):
                    decon_texts.append((sentence1, general_sen, target))

        if not decon_texts:
            decon_texts.append((sentence1, sentence2, target))

        if len(decon_texts) > self.max_outputs:
            decon_texts = decon_texts[:self.max_outputs]


        return decon_texts


if __name__ == '__main__':
    sentence1 = "American Airlines began laying off hundreds of flight attendants on Tuesday, after a federal judge turned aside a union’s bid to block the job losses"
    sentence2 = "American Airlines will recall hundreds of flight attendants as it steps up the number of flights it operates"
    label = "Contradiction"
    decon = Decontextualize()
    print(decon.generate(sentence1, sentence2, label))

