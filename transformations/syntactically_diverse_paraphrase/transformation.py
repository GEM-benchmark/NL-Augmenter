import benepar
import spacy
import nltk
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.syntactically_diverse_paraphrase.sowreap.parse_utils import (
    Sentence,
)
from transformations.syntactically_diverse_paraphrase.sowreap.reap_utils import (
    reapModel,
)
from transformations.syntactically_diverse_paraphrase.sowreap.sow_utils import (
    sowModel,
)
from initialize import spacy_nlp


class ParaphraseSowReap(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["syntactic", "transformer-based", "high-generations"]
    heavy = True

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.sow = sowModel("tanyagoyal/paraphrase-sow", max_outputs)
        self.reap = reapModel("tanyagoyal/paraphrase-reap", max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        try:
            nltk.data.find(f"models/benepar_en3")
        except LookupError:
            benepar.download('benepar_en3')

        if spacy.__version__.startswith("2"):
            self.nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
        else:
            self.nlp.add_pipe("benepar", config={"model": "benepar_en3"})
        self.max_outputs = max_outputs

    def generate(self, sentence: str):
        # use benepar model to retrieve the constituency parse (as a string)
        parse = list(self.nlp(sentence).sents)[0]._.parse_string
        sentence_parsed = Sentence(parse)
        reorderings = self.sow.get_reorderings(sentence_parsed)
        if len(reorderings) == 0:
            return []
        transformations = self.reap.get_transformations(
            sentence_parsed, reorderings
        )
        return transformations


if __name__ == "__main__":

    tf = ParaphraseSowReap(max_outputs=10)

    sentence = "the company withdrew its application on the 196th day its submission ."
    output = tf.generate(sentence)
    print(output)
