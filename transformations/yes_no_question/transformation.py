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


def uncapitalize(string: str):
    if len(string):
        return string[0].lower() + string[1:]
    return ''


def front_auxiliary(auxiliary: Token) -> str:
    if auxiliary.text == "'d":
        if 'Part' in auxiliary.head.morph.get('VerbForm'):
            return 'Had'
        else:
            return 'Would'
    elif auxiliary.text == "'s":
        if 'Past' in auxiliary.head.morph.get('Tense'):
            return 'Has'
        else:
            return 'Is'
    elif auxiliary.text == "'ve":
        return 'Have'
    elif auxiliary.text == "'ll":
        return 'Will'
    else:
        return auxiliary.text.capitalize()


def front_be_verb(be_verb: Token) -> str:
    if be_verb.text == "'s":
        return 'Is'
    elif be_verb.text == "'re":
        return 'Are'
    elif be_verb.text == "'m":
        return 'Am'
    else:
        return be_verb.text.capitalize()


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
        subject_head = None
        for child in verb_head.children:
            if child.dep == nsubj:
                subject_head = child
                break
        subject_phrase_tokens = [t.text_with_ws if t.pos == PROPN
                                 else uncapitalize(t.text_with_ws)
                                 for t in subject_head.subtree]
        subject_phrase = ''.join(subject_phrase_tokens).strip()

        # Get pre-verb adverbs, etc. (expand "n't" to "not"):
        all_left_tokens = doc[:verb_head.i]
        head_left_tokens = [token for token in all_left_tokens if
                            token != subject_head and subject_head not in
                            token.ancestors and token != auxiliary and
                            auxiliary not in token.ancestors]
        head_left = ''.join('not ' if token.text == "n't" and token.head in
                            (verb_head, auxiliary) else
                            uncapitalize(token.text_with_ws) for token in
                            head_left_tokens).strip()

        # Get object, adverbs, prep. phrases, etc. (expand "n't" to "not"):
        # FIXME: I think we have to fix contractions here
        head_right = ''.join('not ' if token.text == "n't" and token.head in
                             (verb_head, auxiliary) else token.text_with_ws
                             for token in doc[verb_head.i + 1:])
        # Change last token to "?"
        if len(head_right) and head_right[-1] in {'.', '!'}:
            head_right = head_right[:-1]
        head_right += '?'

        # Make the question:
        # If there is an auxiliary, make q: [AUX] [SUBJ] [LEFT] [VERB] [RIGHT]
        if auxiliary is not None:
            new_auxiliary = front_auxiliary(auxiliary)
            questions = [
                self.detokenizer.detokenize(
                    filter(len, [new_auxiliary, subject_phrase, head_left,
                                 verb_head.text, head_right]))]

        # If it's a be verb, make q: [BE] [SUBJ] [LEFT] [RIGHT]
        elif verb_head.lemma == self.nlp.vocab.strings['be']:
            new_be_verb = front_be_verb(verb_head)
            questions = [
                self.detokenizer.detokenize(
                    filter(len, [new_be_verb, subject_phrase, head_left,
                                 head_right]))]

        # All other verbs, make q: [DO] [SUBJ] [LEFT] [VERB] [RIGHT]
        else:
            morph = verb_head.morph.to_dict()
            tense = morph.get('Tense')
            if tense == 'Past':
                auxiliary = 'Did'
            elif morph.get('Person') == 'Three' and \
                    morph.get('Number') == 'Sing':
                auxiliary = 'Does'
            else:
                auxiliary = 'Do'
            infinitive = verb_head._.inflect('VB')
            questions = [self.detokenizer.detokenize(
                filter(len, [auxiliary, subject_phrase, head_left, infinitive,
                             head_right]))]

        return questions
