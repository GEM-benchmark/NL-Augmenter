import random
import stanza

stanza.download("en")

import nltk

nltk.download("wordnet")

from nltk.corpus import wordnet
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import re

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    ref: https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py#L28
    """
    text = " ".join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace(". . .", "...")
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r" ([.,:;?!%]+)$", r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


def synonym_substitution(text, stanza_pipeline, seed=42, prob=0.5, max_outputs=1):
    random.seed(seed)
    upos_wn_dict = {
        "VERB": "v",
        "NOUN": "n",
        "ADV": "r",
        "ADJ": "s",
    }

    doc = stanza_pipeline(text)
    results = []
    for _ in range(max_outputs):
        result = []
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
        # detokenize sentences
        result = untokenize(result)
        if result not in results:
            # make sure there is no dup in results
            results.append(result)
    return results


"""
Substitute words with synonyms using stanza (for POS) and wordnet via nltk (for synonyms)
"""


class SynonymSubstitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=42, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.stanza_pipeline = stanza.Pipeline("en", processors="tokenize,mwt,pos")
        self.prob = prob

    def generate(self, sentence: str):
        perturbed = synonym_substitution(
            text=sentence,
            stanza_pipeline=self.stanza_pipeline,
            seed=self.seed,
            prob=self.prob,
            max_outputs=self.max_outputs,
        )
        return perturbed
