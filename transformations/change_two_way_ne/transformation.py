import numpy as np
import re

from checklist.perturb import Perturb

from interfaces.SentenceOperation import SentenceAndTargetOperation
import spacy
from tasks.TaskTypes import TaskType


class ChangeTwoWayNe(SentenceAndTargetOperation):
    """
    Repository of names has been taken from the CheckList repo.
    @TODO - need to extend this to other NEs like location, etc.
    @TODO - also this needs to move into a separate folder.
    """

    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    tgt_languages = ["en"]

    def __init__(self, first_only=False, last_only=False, n=1, seed=0):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.first_only = first_only  # first name
        self.last_only = last_only  # last name
        self.n = n

    def generate(self, sentence: str, target: str):
        np.random.seed(self.seed)
        perturbed_source = sentence
        perturbed_target = target
        n = self.n
        doc = self.nlp(sentence).doc
        # (1) replace person entities
        person_entities = [
            x.text for x in doc.ents if np.all([a.ent_type_ == "PERSON" for a in x])
        ]
        ret = []
        ret_m = []
        outs = []
        for x in person_entities:
            f = x.split()[0]
            sex = None
            if f.capitalize() in Perturb.data["name_set"]["women"]:
                sex = "women"
            if f.capitalize() in Perturb.data["name_set"]["men"]:
                sex = "men"
            if not sex:
                continue
            if len(x.split()) > 1:
                l = x.split()[1]
                if (
                        len(l) > 2
                        and l.capitalize() not in Perturb.data["name_set"]["last"]
                ):
                    continue
            else:
                if self.last_only:
                    return None
            names = Perturb.data["name"][sex][: 90 + n]
            to_use = np.random.choice(names, n)
            if not self.first_only:
                f = x
                if len(x.split()) > 1:
                    last = Perturb.data["name"]["last"][: 90 + n]
                    last = np.random.choice(last, n)
                    to_use = ["%s %s" % (x, y) for x, y in zip(names, last)]
                    if self.last_only:
                        to_use = last
                        f = x.split()[1]
            for y in to_use:
                to_replace = r"\b%s\b" % re.escape(f)
                ret.append(re.sub(to_replace, y, doc.text))
                outs.append(
                    re.sub(to_replace, y, target)
                )  # this is the part added from Checklist
                ret_m.append((f, y))
        if len(ret) > 0 and ret[0] != sentence:
            perturbed_source = ret[0]
            perturbed_target = outs[0]
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}\nLabel: {perturbed_target}"
            )
            return perturbed_source, perturbed_target

        # (2) add location named entities
        ents = [x.text for x in doc.ents if np.all([a.ent_type_ == "GPE" for a in x])]
        ret = []
        ret_m = []
        outs = []
        for x in ents:
            if x in Perturb.data["city"]:
                names = Perturb.data["city"][:100]
            elif x in Perturb.data["country"]:
                names = Perturb.data["country"][:50]
            else:
                continue
            sub_re = re.compile(r"\b%s\b" % re.escape(x))
            to_use = np.random.choice(names, n)
            ret.extend([sub_re.sub(n, doc.text) for n in to_use])
            outs.extend([sub_re.sub(n, target) for n in to_use])
            ret_m.extend([(x, n) for n in to_use])
        if len(ret) > 0 and ret[0] != sentence:
            perturbed_source = ret[0]
            perturbed_target = outs[0]
        if self.verbose:
            print(
                f"Perturbed Input from {self.name()} : \nSource: {perturbed_source}\nLabel: {perturbed_target}"
            )
        return perturbed_source, perturbed_target


"""

# Sample code to demonstrate adding test cases.

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = ChangeTwoWayNe()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    src = ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate" 
                     " to indicate the relation between two or more arguments."]
    tgt = ["Andrew did not return the French book to Chris that was bought earlier",
                     "Gapped sentences such as Paul likes coffee and Mary tea, lack an overt predicate!",]
    for sentence, target in zip(src, tgt):
        sentence_o, target_o = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": {"sentence": sentence_o, "target": target_o}}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
