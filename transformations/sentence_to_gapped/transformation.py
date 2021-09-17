import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

import spacy
from spacy.tokens.token import Token

"""
Homophone perturbation
"""

class SentenceToGapped(SentenceOperation):
    """
    Some code adapted from the Python Natural Language Processing Cookbook, https://shrtm.nu/suAC
    """
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["en"]

    def __init__(self, seed: int = 0) -> None:
        max_outputs=1
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.nlp = spacy.load('en_core_web_sm')
        self.conj_pos = "CCONJ"
        self.verb_pos = "VERB"

    def find_root_of_sentence(self, sentence: str):
        root_token = None
        for token in sentence:
            if token.dep_ == "ROOT":
                root_token = token
                break
        return root_token

    def find_other_verbs(self, sentence: str, root_token: Token):
        other_verbs = []
        for token in sentence:
            ancestors = list(token.ancestors)
            if token.pos_ == "VERB" and len(ancestors) == 1 and ancestors[0] == root_token:
                other_verbs.append(token)
        return other_verbs

    def get_clause_token_span_for_verb(self, verb: Token, sentence: str, all_verbs: List[Token]):
        first_token_index = len(sentence)
        last_token_index = 0
        this_verb_children = list(verb.children)
        for child in this_verb_children:
            if child not in all_verbs:
                if child.i < first_token_index:
                    first_token_index = child.i
                if child.i > last_token_index:
                    last_token_index = child.i
        return first_token_index, last_token_index

    def get_verbs(self, clause: str):
        verbs = [token.text for token in self.nlp(clause) if token.pos_ == self.verb_pos]
        return len(verbs), verbs

    def get_clauses(self, sentence: str):
        import ipdb
        ipdb.set_trace()
        doc = self.nlp(sentence)
        conjunctions = [token for token in doc if token.pos_ == self.conj_pos]

        root_token = self.find_root_of_sentence(doc)
        other_verbs = self.find_other_verbs(doc, root_token)

        token_spans = []
        all_verbs = [root_token] + other_verbs
        for other_verb in all_verbs:
            token_spans.append(self.get_clause_token_span_for_verb(other_verb, doc, all_verbs))

        ipdb.set_trace()
        sentence_clauses = []
        for token_span in token_spans:
            start, end = token_span
            if (start < end):
                clause = doc[start:end]
                sentence_clauses.append(clause)
        ipdb.set_trace()
        clauses_texts = [clause.text for clause in sentence_clauses]

        gapped_sentence = ""

        for c_idx, clause in enumerate(clauses_texts):

            # If the clause has the same verb as the previous clause, and there is only 1 verb, delete it
            if c_idx == 0:
                gapped_sentence += clause
            else:
                num_verbs_1, verbs_1 = self.get_verbs(clauses_texts[c_idx-1])
                num_verbs_2, verbs_2 = self.get_verbs(clauses_texts[c_idx])
                if num_verbs_1 == num_verbs_2 == 1:
                    gapped_sentence += ' ' + clause.replace(verbs_1[0] + ' ', '')
                else:
                    gapped_sentence += ' ' + clause

            if c_idx < len(conjunctions):
                gapped_sentence += ' ' + conjunctions[c_idx].text

        print(gapped_sentence)
        return gapped_sentence

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)


        return gapped_sentence
