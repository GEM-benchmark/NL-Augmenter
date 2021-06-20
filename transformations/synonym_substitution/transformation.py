import random
import stanza

stanza.download("en")
import nltk

nltk.download("wordnet")
from nltk.corpus import wordnet
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def synonym_substitution(text, stanza_pipeline, seed=42, prob=0.5):
    random.seed(seed)
    upos_wn_dict = {
        "VERB": "v",
        "NOUN": "n",
        "ADV": "r",
        "ADJ": "s",
    }
    result = []
    doc = stanza_pipeline(text)
    for sent in doc.sentences:
        for word_dict in sent.words:
            word = word_dict.text
            wn_pos = upos_wn_dict.get(word_dict.upos)
            if wn_pos is None:
                result.append(word)
            else:
                syns = wordnet.synsets(word, pos=wn_pos)
                syns = [syn.name().split(".")[0] for syn in syns]
                syns = [syn for syn in syns if syn != word]
                if len(syns) > 0 and random.random() < prob:
                    result.append(random.choice(syns).replace("_", " "))
                else:
                    result.append(word)
    return " ".join(result)


"""
Substitute words with synonyms using stanza (for POS) and wordnet via nltk (for synonyms)
"""


class SynonymSubstitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, prob=0.5):
        super().__init__(seed)
        self.stanza_pipeline = stanza.Pipeline("en", processors="tokenize,mwt,pos")
        self.prob = prob

    def generate(self, sentence: str):
        pertubed = synonym_substitution(
            text=sentence,
            stanza_pipeline=self.stanza_pipeline,
            seed=self.seed,
            prob=self.prob,
        )
        return pertubed
