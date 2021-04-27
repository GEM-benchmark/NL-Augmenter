import random
import numpy as np
import re

from checklist.perturb import Perturb

from transformations.SentenceTransformation import SentenceTransformation, SentenceAndLabelTransformation
import spacy


class ChangeNamedEntities(SentenceTransformation):

    def __init__(self, n=1):
        # TODO: Do not repeat parse computations.
        random.seed(0)
        self.nlp = spacy.load('en_core_web_sm')
        self.n = n

    def generate(self, sentence: str):
        np.random.seed(0)
        pertubed = Perturb.perturb([self.nlp(sentence)], Perturb.change_names, nsamples=1)
        pertubed = pertubed.data[0][1]
        print(f"Perturbed Input from {self.name()} : {pertubed}")
        return pertubed


class ChangeTwoWayNamedEntities(SentenceAndLabelTransformation):
    '''
        Repository of names has been taken from the CheckList repo.
        @TODO - need to extend this to other NEs like location, etc.
    '''

    def __init__(self, first_only=False, last_only=False, n=1):
        np.random.seed(0)
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


if __name__ == '__main__':
    tr = ChangeTwoWayNamedEntities()
    tr.generate("Andrew played football with Chris", "Andrew seldom played football with Chris.")
