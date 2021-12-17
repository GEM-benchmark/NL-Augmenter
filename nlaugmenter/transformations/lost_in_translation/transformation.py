import random

from datasets import load_metric
from transformers import pipeline

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class LostInTranslation(SentenceOperation):
    """
    Repeated translation of input text
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    # languages = ["en"]
    heavy = True

    def __init__(
        self,
        seed=0,
        langs=["es", "de", "zh", "fr", "ru"],
        how="strict",
        layers=5,
        max_length=600,
        max_outputs=1,
        device=-1,
        scorer="rougeL",
        min_score=-1,
    ):
        """
        seed: set to None to disable
        langs: list of languages, from those supported by OpusMT
        how:
          "strict" for static list order,
          "shuffle" to shuffle said list,
          "random" to draw (layers) times with replacement
        device: use CPU (-1) or GPU (>=0)
        layers: number of encode/decode operations to perform
        max_length: this is passed to pipeline
        max_outputs: this is passed to super
        scorer: of rouge1, rouge2, etc.
        min_score: terminate and return if score drops below this threshold
        """
        super().__init__(seed, max_outputs)
        self.langs = langs
        self.how = how
        self.device = device
        self.layers = layers
        self.max_length = max_length
        self.scorer = scorer
        self.min_score = min_score

    def encode_decode(self, text, lang, max_length=600, device=-1):
        # translate and un-translate
        # using Helsinki-NLP OpusMT models
        encode = pipeline(
            "translation_en_to_{}".format(lang),
            model="Helsinki-NLP/opus-mt-en-{}".format(lang),
            device=device,
        )
        decode = pipeline(
            "translation_{}_to_en".format(lang),
            model="Helsinki-NLP/opus-mt-{}-en".format(lang),
            device=device,
        )
        # en->lang->en
        return decode(
            encode(text, max_length=max_length)[0]["translation_text"],
            max_length=max_length,
        )[0]["translation_text"]

    def shell(
        self, text, langs, how, layers, max_length, device, scorer, min_score
    ):
        # repeated encode_decode cycles
        # according to self.how
        if how == "random":
            # choose a random transformation from the given set
            for i in range(layers):
                target = random.choice(langs)
                text = self.encode_decode(text, target, max_length, device)
                if min_score > 0:
                    # TODO: Unresolved reference orig. (Needs to be fix)
                    if self.similarity(orig, text, scorer) < min_score:
                        break
        else:
            if how == "shuffle":
                # shuffle the input list
                langs = random.shuffle(langs)
            for i in range(layers):
                # if layers > len(langs).
                # restart at beginning of list
                target = langs[i % len(langs)]
                text = self.encode_decode(text, target, max_length, device)
                if min_score > 0:
                    if self.similarity(orig, text, scorer) < min_score:
                        break
        return text

    def similarity(self, ref, pred, scorer):
        metric = load_metric("rouge")
        metric.add(reference=ref, prediction=pred)
        score = metric.compute()
        return score[scorer][0].fmeasure

    def generate(self, sentence: str):
        # call shell, which applies the layers
        return [
            self.shell(
                sentence,
                self.langs,
                self.how,
                self.layers,
                self.max_length,
                self.device,
                self.scorer,
                self.min_score,
            )
        ]


# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
# if __name__ == '__main__':
#    import json
#    from TestRunner import convert_to_snake_case
#
#    tf = LostInTranslation(max_outputs=3)
#    sentence = "Andrew finally returned the French book to Chris that I bought last week"
#    test_cases = []
#    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
#                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
#                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
#                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
#                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
#        test_cases.append({
#            "class": tf.name(),
#            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
#        )
#    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#    #print(json.dumps(json_file))
#    with open('test.json','w') as outfile:
#        json.dump(json_file,outfile,indent=4)
