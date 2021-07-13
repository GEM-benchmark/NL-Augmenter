import spacy
from typing import Union
from initialize import spacy_nlp
import pyinflect
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spacy.symbols import nsubj, aux, PROPN
from spacy.tokens import Token
from spacy.tokens.doc import Doc

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class YesNoQuestionPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.detokenizer = TreebankWordDetokenizer()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load('en_core_web_sm')

    def generate(self, sentence: str):
        # TODO: Handle compound sentences
        doc: Doc = self.nlp(sentence)

        # Look for sentence verb head, starting with first token
        verb_head: Token = doc[0]
        while verb_head != verb_head.head:
            verb_head = verb_head.head

        # Look for auxiliary verb
        auxiliary: Union[Token, str, None] = None
        for child in verb_head.children:
            if child.dep == aux:
                auxiliary = child

        # Look for root token of subject
        subject_head, subject_phrase_tokens = None, []
        for child in verb_head.children:
            if child.dep == nsubj:
                subject_head = child
                subject_phrase_tokens = [str(t) if t.pos != PROPN else
                                         str(t).lower() for t in
                                         subject_head.subtree]
                break

        # Get object, adverbs, prepositional phrases, etc.:
        # FIXME: I think we have to fix contractions here
        etc = [str(token) for right in verb_head.rights for token in
               right.subtree]
        # Change last token to "?"
        if len(etc) and etc[-1] in {'.', '!'}:
            etc[-1] = '?'
        else:
            etc.append('?')

        # Make the question:
        # If there is an auxiliary, make q: [AUX] [SUBJ] [VERB] [ETC]
        if auxiliary is not None:
            tokens = [str(auxiliary).capitalize()] + subject_phrase_tokens + \
                     [verb_head._.inflect('VB')] + etc
            questions = [self.detokenizer.detokenize(tokens)]

        # If it's a be verb, make q: [BE] [SUBJ] [ETC]
        elif verb_head.lemma == self.nlp.vocab.strings['be']:
            tokens = [str(verb_head)] + subject_phrase_tokens + etc
            questions = [self.detokenizer.detokenize(tokens)]

        # All other verbs, make q: [DO] [SUBJ] [VERB] [ETC]
        else:
            morph = verb_head.morph.to_dict()
            tense = morph['Tense']
            if tense == 'Past':
                auxiliary = 'Did'
            elif morph['Person'] == 'Three' and morph['Number'] == 'Sing':
                auxiliary = 'Does'
            else:
                auxiliary = 'Do'
            infinitive = verb_head._.inflect('VB')

            tokens = [auxiliary] + subject_phrase_tokens + [infinitive] + etc
            questions = [self.detokenizer.detokenize(tokens)]

        return questions


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = ButterFingersPerturbation(max_outputs=3)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
