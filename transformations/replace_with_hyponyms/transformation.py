import numpy as np
import spacy
#from checklist.perturb import Perturb
from checklist.editor import Editor

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ReplaceHyponyms(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, n=1, seed=0, max_output=2):
        # TODO: Do not repeat parse computations.
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.n = n
        self.max_output = max_output

    def generate(self, sentence: str):
        np.random.seed(self.seed)
        words = []
        perturbed_texts = []
        tokens = self.nlp(sentence)
        for token in tokens:
            if token.pos_ == 'NOUN':
              words.append(token)
              hyp_list = editor.hyponyms(sentence, token)
              for hyp in hyp_list:
              #if len(hyp_list)>0:
                #Replace the noun with the hyponym
                #perturbed_texts.append(sentence.replace('token',hyp_list[0]))
                perturbed_texts.append(sentence.replace('token',hyp))
              if len(perturbed_texts>=max_output):
                break
        '''
        perturbed = Perturb.perturb(
            [self.nlp(sentence)], Perturb.change_names, nsamples=1
        )
        '''
        perturbed_texts = (
            perturbed_texts[: self.max_output]
            if len(perturbed_text) > 0
            else [sentence]
        )
        return perturbed_texts
