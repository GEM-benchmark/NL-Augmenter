import spacy

from common.initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
The code is partially adapted and modified from https://github.com/NSchrading/intro-spacy-nlp
"""


class Summarization(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    keywords = ["parser-based", "possible-meaning-alteration", "rule-based"]

    def __init__(self):
        # super().__init__(seed, max_outputs=max_outputs)
        self.nlp = (
            spacy_nlp
            if spacy_nlp
            else spacy.load("en_core_web_sm", disable=["ner", "textcat"])
        )
        self.dicts = {
            "SUBJECTS": [
                "nsubj",
                "nsubjpass",
                "csubj",
                "csubjpass",
                "agent",
                "expl",
            ],
            "OBJECTS": [
                "dobj",
                "dative",
                "attr",
                "oprd",
                "acomp",
                "advcl",
                "advmod",
                "amod",
                "appos",
                "nn",
                "nmod",
                "ccomp",
                "complm",
                "hmod",
                "infmod",
                "xcomp",
                "rcmod",
                "poss",
                " possessive",
            ],
            "COMPOUNDS": ["compound"],
            "PREPOSITIONS": ["prep"],
        }

    def generate(self, sentence: str):
        sequence = self.nlp(sentence)
        summarization_texts = self.Summarize(sequence)
        return summarization_texts

    def Summarize(self, tokens):
        """
        this algorithm is based on the dependence tree parsing. When the input sentence comes, we would first find the verbs and root token. If verbs exist, it would be easily to find the subject and object,
        otherwise, we will split the sentence based on the root token.
        """
        results = []
        verbs = [
            tok
            for tok in tokens
            if tok.pos_ == "VERB" or tok.pos_ == "AUX" or tok.dep_ == "aux"
        ]
        roots = [tok for tok in tokens if tok.dep_ == "ROOT"]
        checks = [0 for tok in verbs if tok.dep_ == "ROOT"]
        if 0 in checks:
            for v in verbs:
                subs, verbNegated = self.getAllSubs(v)
                if len(subs) > 0:
                    v, objs = self.getAllObjs(v)
                    for sub in subs:
                        for obj in objs:
                            objNegated = self.isNegated(obj)
                            results.append(
                                sub.text
                                + " "
                                + (
                                    "!" + v.text
                                    if verbNegated or objNegated
                                    else v.text
                                )
                                + " "
                                + obj.text
                            )
            # print(', '.join(results))

        else:
            for root in roots:
                v = None
                subs, rootNegated = [root], self.isNegated(root)
                if len(subs) > 0:
                    for term in root.rights:
                        if term.pos_ in ["VERB", "AUX"]:
                            v = term
                    if v is not None:
                        v, objs = self.getAllObjs(v)
                        for sub in subs:
                            for obj in objs:
                                objNegated = self.isNegated(obj)
                                results.append(
                                    sub.text
                                    + " "
                                    + (
                                        "!" + v.text
                                        if rootNegated or objNegated
                                        else v.text
                                    )
                                    + " "
                                    + obj.text
                                )
                    else:
                        continue

        final_results = [", ".join(results)]
        return final_results

    def getSubsFromConjunctions(self, subs):
        """
        search the subject when meet the conjuntions
        """
        moreSubs = []
        for sub in subs:
            # rights is a generator
            rights = list(sub.rights)
            rightDeps = {tok.lower_ for tok in rights}
            if "and" in rightDeps:
                moreSubs.extend(
                    [
                        tok
                        for tok in rights
                        if tok.dep_ in self.dicts["SUBJECTS"]
                        or tok.pos_ == "NOUN"
                    ]
                )
                if len(moreSubs) > 0:
                    moreSubs.extend(self.getSubsFromConjunctions(moreSubs))
        return moreSubs

    def isNegated(self, tok):
        """
        Check if verbs are negated
        """
        negations = {"no", "not", "n't", "never", "none"}
        for dep in list(tok.lefts) + list(tok.rights):
            if dep.lower_ in negations:
                return True
        return False

    def getObjsFromPrepositions(self, deps):
        """
        Not all objects come after the verbs, this function would double check if there exist prepositions, and check its next word
        """
        objs = []
        for dep in deps:
            if dep.pos_ == "ADP" and dep.dep_ == "prep":
                objs.extend(
                    [
                        tok
                        for tok in dep.rights
                        if tok.dep_ in self.dicts["OBJECTS"]
                        or (tok.pos_ == "PRON" and tok.lower_ == "me")
                    ]
                )
                potentialNewVerb, potentialNewObjs = self.getObjFromXComp(
                    dep.rights
                )
                if (
                    potentialNewVerb is not None
                    and potentialNewObjs is not None
                    and len(potentialNewObjs) > 0
                ):
                    objs.extend(potentialNewObjs)
        return objs

    def getObjFromXComp(self, deps):
        for dep in deps:
            if dep.pos_ == "VERB" and (
                dep.dep_ == "xcomp" or dep.dep_ == "pcomp"
            ):
                v = dep
                rights = list(v.rights)
                objs = [
                    tok for tok in rights if tok.dep_ in self.dicts["OBJECTS"]
                ]
                objs.extend(self.getObjsFromPrepositions(rights))
                if len(objs) > 0:
                    return v, objs
        return None, None

    def getObjsFromConjunctions(self, objs):
        """
        Similar with finding subjects with conjunctions
        """
        moreObjs = []
        for obj in objs:
            # rights is a generator
            rights = list(obj.rights)
            rightDeps = {tok.lower_ for tok in rights}
            if "and" in rightDeps:
                moreObjs.extend(
                    [
                        tok
                        for tok in rights
                        if tok.dep_ in self.dicts["OBJECTS"]
                        or tok.pos_ == "NOUN"
                    ]
                )
                if len(moreObjs) > 0:
                    moreObjs.extend(self.getObjsFromConjunctions(moreObjs))
        return moreObjs

    def getVerbsFromConjunctions(self, verbs):
        """
        Sometimes the verbs come with pair with conjunctions, or two clauses connected with conjunctions
        """
        moreVerbs = []
        for verb in verbs:
            rightDeps = {tok.lower_ for tok in verb.rights}
            if "and" in rightDeps:
                moreVerbs.extend(
                    [tok for tok in verb.rights if tok.pos_ == "VERB"]
                )
                if len(moreVerbs) > 0:
                    moreVerbs.extend(self.getVerbsFromConjunctions(moreVerbs))
        return moreVerbs

    def findSubs(self, tok):
        """
        Based on the verbs, search backwards to find the subjects
        """
        head = tok.head
        while (
            head.pos_ != "VERB" and head.pos_ != "NOUN" and head.head != head
        ):
            head = head.head
        if head.pos_ == "VERB":
            subs = [tok for tok in head.lefts if tok.dep_ == "SUB"]
            if len(subs) > 0:
                verbNegated = self.isNegated(head)
                subs.extend(self.getSubsFromConjunctions(subs))
                return subs, verbNegated
            elif head.head != head:
                return self.findSubs(head)
        elif head.pos_ == "NOUN":
            return [head], self.isNegated(tok)
        return [], False

    def getAllSubs(self, v):
        verbNegated = self.isNegated(v)
        subs = [
            tok
            for tok in v.lefts
            if tok.dep_ in self.dicts["SUBJECTS"] and tok.pos_ != "DET"
        ]
        if len(subs) > 0:
            subs.extend(self.getSubsFromConjunctions(subs))
        else:
            foundSubs, verbNegated = self.findSubs(v)
            subs.extend(foundSubs)
        return subs, verbNegated

    def getAllObjs(self, v):
        rights = list(v.rights)
        objs = [tok for tok in rights if tok.dep_ in self.dicts["OBJECTS"]]
        objs.extend(self.getObjsFromPrepositions(rights))

        potentialNewVerb, potentialNewObjs = self.getObjFromXComp(rights)
        if (
            potentialNewVerb is not None
            and potentialNewObjs is not None
            and len(potentialNewObjs) > 0
        ):
            objs.extend(potentialNewObjs)
            v = potentialNewVerb
        if len(objs) > 0:
            objs.extend(self.getObjsFromConjunctions(objs))
        return v, objs


# # Sample code to demonstrate usage. Can also assist in adding test cases.
# # You don't need to keep this code in your transformation.
# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case
#     tf = Summarization()
#     test_cases = []
#     for sentence in ["Apple is looking at buying U.K. startup which costs me for $132 billion.",
#                      "Parsley Energy to acquire Jagged Peak Energy Company in an all-stock deal.",
#                      "Stillwater is not a 2010 American live-action/animated dark fantasy adventure film",
#                      "Andrew finally returned the French book to Chris that I bought last week",
#                      "Jack was the leader of the team, but Harry is better than him."]:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
#         )
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json.dumps(json_file, indent=2))
