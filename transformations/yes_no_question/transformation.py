import spacy
from typing import Union, List
from initialize import spacy_nlp
import pyinflect
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spacy.symbols import aux, cc, nsubj, AUX, NOUN, PRON, PROPN, VERB
from spacy.tokens import Token, Span
from spacy.tokens.doc import Doc

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def uncapitalize(string: str):
    """De-capitalize first character of string

    E.g. 'How is Michael doing?' -> 'how is Michael doing?'
    """
    if len(string):
        return string[0].lower() + string[1:]
    return ''


def front_auxiliary(auxiliary: Token) -> str:
    """Take auxiliary (type: spacy Token) and return capitalized, expanded
    (i.e. un-contracted) auxiliary (type: str). Differentiates certain English
    identical English contractions (e.g. "'d", "'s") using morphology data
    stored in auxiliary `Token` object.

    E.g.:
    - <Token 'has'> -> 'Has'
    - <Token "'ve"> -> 'Have'
    """
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
    """Take be verb (type: spacy Token), return capitalized, expanded (i.e.
    un-contracted) form.

    E.g.:
    - <Token 'is'> -> 'Is'
    - <Token "'re"> -> 'Are'
    """
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
        TaskType.QUESTION_ANSWERING,
        TaskType.QUESTION_GENERATION
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.detokenizer = TreebankWordDetokenizer()
        self.nlp = spacy_nlp if spacy_nlp else spacy.load('en_core_web_sm')

    def statement_to_question(self, sentence: Span) -> Union[str, None]:
        """Given a statement (type: spacy Span), convert to corresponding
        yes-or-no question.
        """
        # Look for sentence verb head, starting with first token
        verb_head: Token = sentence[0]
        while verb_head != verb_head.head:
            verb_head = verb_head.head
        # Give up on sentence if POS tag doesn't match dependency tag
        if verb_head.pos not in {AUX, VERB}:
            return None

        # If there's a coordinating conjunction, give up
        for child in verb_head.children:
            if child.dep == cc:
                return None

        # Look for auxiliary verb
        auxiliary: Union[Token, str, None] = None
        for child in verb_head.children:
            if child.dep == aux:
                auxiliary = child
        # Give up on sentence if POS tag doesn't match dependency tag
        if auxiliary is not None and auxiliary.pos != AUX:
            return None

        # Look for root token of subject
        for child in verb_head.children:
            if child.dep == nsubj:
                subject_head = child
                break
        # If there's no root subject, just give up
        else:
            return None
        # Give up on sentence if POS tag doesn't match dependency tag
        if subject_head.pos not in {NOUN, PROPN, PRON}:
            return None
        subject_phrase_tokens = [t.text_with_ws if t.pos == PROPN
                                 else uncapitalize(t.text_with_ws)
                                 for t in subject_head.subtree]
        subject_phrase = ''.join(subject_phrase_tokens).strip()

        # Get pre-verb adverbs, etc. (expand "n't" to "not"):
        all_left_tokens = sentence[:verb_head.i - sentence.start]
        head_left_tokens = [token for token in all_left_tokens if
                            token != subject_head and subject_head not in
                            token.ancestors and token != auxiliary and
                            auxiliary not in token.ancestors]
        head_left = ''.join('not ' if token.text == "n't" and token.head in
                                      (verb_head, auxiliary) else
                            uncapitalize(token.text_with_ws) for token in
                            head_left_tokens).strip()

        # Get object, adverbs, prep. phrases, etc. (expand "n't" to "not"):
        head_right = ''.join('not ' if token.text == "n't" and token.head in
                                       (verb_head,
                                        auxiliary) else token.text_with_ws
                             for token in sentence[verb_head.i + 1 -
                                                   sentence.start:]).strip()

        # Change last token to "?"
        if len(head_right) and head_right[-1] in {'.', '!'}:
            head_right = head_right[:-1]
        head_right += '?'

        # Make the question:
        # If there is an auxiliary, make q: [AUX] [SUBJ] [LEFT] [VERB] [RIGHT]
        if auxiliary is not None:
            new_auxiliary = front_auxiliary(auxiliary)
            question = self.detokenizer.detokenize(
                filter(len, [new_auxiliary, subject_phrase, head_left,
                             verb_head.text, head_right]))

        # If it's a be verb, make q: [BE] [SUBJ] [LEFT] [RIGHT]
        elif verb_head.lemma == self.nlp.vocab.strings['be']:
            new_be_verb = front_be_verb(verb_head)
            question = self.detokenizer.detokenize(
                filter(len, [new_be_verb, subject_phrase, head_left,
                             head_right]))

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
            question = self.detokenizer.detokenize(
                filter(len, [auxiliary, subject_phrase, head_left, infinitive,
                             head_right]))

        """
        if sentence.text == "He'd gone to the store with Michael two days earlier.":
            raise Exception([(token.text_with_ws, token.dep_, token.pos_,
                              token.morph) for token in sentence])
        """

        return question

    def generate(self, sentence: str) -> List[str]:
        doc: Doc = self.nlp(sentence)

        questions: List[str] = []
        for sentence in doc.sents:
            # TODO: Test if sentence is statement or question
            question = self.statement_to_question(sentence)
            if question is not None:
                questions.append(question)

        return questions
