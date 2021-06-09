import numpy as np
import re

from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceAndTargetOperation
import spacy
from tasks.TaskTypes import TaskType


class ChangeTwoWayNamedEntities(SentenceAndTargetOperation):
    '''
        Repository of names has been taken from the CheckList repo.
        @TODO - need to extend this to other NEs like location, etc.
        @TODO - also this needs to move into a separate folder.
    '''
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    src_locales = ["en"]
    tgt_locales = ["en"]

    def __init__(self, first_only=False, last_only=False, n=1, seed=0):
        super().__init__(seed)

        np.random.seed(self.seed)
        self.nlp = spacy.load('en_core_web_sm')
        self.first_only = first_only  # first name
        self.last_only = last_only  # last name
        self.n = n

    def generate(self, sentence: str, output_sequence: str):
        perturbed_source = sentence
        perturbed_target = output_sequence
        n = self.n
        doc = self.nlp(sentence).doc
        # (1) replace person entities
        person_entities = [x.text for x in doc.ents if np.all([a.ent_type_ == 'PERSON' for a in x])]
        ret = []
        ret_m = []
        outs = []
        for x in person_entities:
            f = x.split()[0]
            sex = None
            if f.capitalize() in Perturb.data['name_set']['women']:
                sex = 'women'
            if f.capitalize() in Perturb.data['name_set']['men']:
                sex = 'men'
            if not sex:
                continue
            if len(x.split()) > 1:
                l = x.split()[1]
                if len(l) > 2 and l.capitalize() not in Perturb.data['name_set']['last']:
                    continue
            else:
                if self.last_only:
                    return None
            names = Perturb.data['name'][sex][:90 + n]
            to_use = np.random.choice(names, n)
            if not self.first_only:
                f = x
                if len(x.split()) > 1:
                    last = Perturb.data['name']['last'][:90 + n]
                    last = np.random.choice(last, n)
                    to_use = ['%s %s' % (x, y) for x, y in zip(names, last)]
                    if self.last_only:
                        to_use = last
                        f = x.split()[1]
            for y in to_use:
                to_replace = r'\b%s\b' % re.escape(f)
                ret.append(re.sub(to_replace, y, doc.text))
                outs.append(re.sub(to_replace, y, output_sequence))  # this is the part added from Checklist
                ret_m.append((f, y))
        if len(ret) > 0 and ret[0] != sentence:
            perturbed_source = ret[0]
            perturbed_target = outs[0]
            print(f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}\nLabel: {perturbed_target}")
            return perturbed_source, perturbed_target

        # (2) add location named entities
        ents = [x.text for x in doc.ents if np.all([a.ent_type_ == 'GPE' for a in x])]
        ret = []
        ret_m = []
        outs = []
        for x in ents:
            if x in Perturb.data['city']:
                names = Perturb.data['city'][:100]
            elif x in Perturb.data['country']:
                names = Perturb.data['country'][:50]
            else:
                continue
            sub_re = re.compile(r'\b%s\b' % re.escape(x))
            to_use = np.random.choice(names, n)
            ret.extend([sub_re.sub(n, doc.text) for n in to_use])
            outs.extend([sub_re.sub(n, output_sequence) for n in to_use])
            ret_m.extend([(x, n) for n in to_use])
        if len(ret) > 0 and ret[0] != sentence:
            perturbed_source = ret[0]
            perturbed_target = outs[0]
        print(f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}\nLabel: {perturbed_target}")
        return perturbed_source, perturbed_target