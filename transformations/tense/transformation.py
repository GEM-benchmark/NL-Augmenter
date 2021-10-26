from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import string
from pattern.en import conjugate, PAST, PRESENT, SINGULAR, PLURAL
import spacy
from spacy.symbols import NOUN
import random
from initialize import spacy_nlp

SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}

def _get_conjuncts(tok):
    """
    Return conjunct dependents of the leftmost conjunct in a coordinated phrase,
    e.g. "Burton, [Dan], and [Josh] ...".
    """
    return [right for right in tok.rights
            if right.dep_ == 'conj']


def is_plural_noun(token):
    """
    Returns True if token is a plural noun, False otherwise.
    Args:
        token (``spacy.Token``): parent document must have POS information
    Returns:
        bool
    """
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    return True if token.pos == NOUN and token.lemma != token.lower else False


def get_subjects_of_verb(verb):
    if verb.dep_ == "aux" and list(verb.ancestors):
        return get_subjects_of_verb(list(verb.ancestors)[0])
    """Return all subjects of a verb according to the dependency parse."""
    subjs = [tok for tok in verb.lefts if tok.dep_ in SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(tok for subj in subjs for tok in _get_conjuncts(subj))
    if not len(subjs):
        ancestors = list(verb.ancestors)
        if len(ancestors) > 0:
            return get_subjects_of_verb(ancestors[0])
    return subjs


def is_plural_verb(token):
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    subjects = get_subjects_of_verb(token)
    if not len(subjects):
        return False
    plural_score = sum([is_plural_noun(x) for x in subjects])/len(subjects)

    return plural_score > .5

def preserve_caps(word, newWord):
    """Returns newWord, capitalizing it if word is capitalized."""
    if word[0] >= 'A' and word[0] <= 'Z':
        newWord = newWord.capitalize()
    return newWord

'''
change tense function borrowed from https://github.com/bendichter/tenseflow/blob/master/tenseflow/change_tense.py
'''

class TenseTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]

    def __init__(self, to_tense):
        super().__init__()
        assert to_tense in ['past', 'present', 'future', 'random']
        self.to_tense = to_tense
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def change_tense(self, text, to_tense):
        """Change the tense of text.
        Args:
            text (str): text to change.
            to_tense (str): 'present','past', or 'future'
            npl (SpaCy model, optional):
        Returns:
            str: changed text.
        """
        tense_lookup = {'future': 'inf', 'present': PRESENT, 'past': PAST}
        tense = tense_lookup[to_tense]

        doc = self.nlp(text)
        print(doc[0], doc)
        out = list()
        out.append(doc[0].text)
        words = []
        for word in doc:
            words.append(word)
            if len(words) == 1:
                continue
            if (words[-2].text == 'will' and words[-2].tag_ == 'MD' and words[-1].tag_ == 'VB') or \
                words[-1].tag_ in ('VBD', 'VBP', 'VBZ', 'VBN') or \
                (not words[-2].text in ('to', 'not') and words[-1].tag_ == 'VB'):

                if words[-2].text in ('were', 'am', 'is', 'are', 'was') or \
                    (words[-2].text == 'be' and len(words) > 2 and words[-3].text == 'will'):
                    this_tense = tense_lookup['past']
                else:
                    this_tense = tense

                subjects = [x.text for x in get_subjects_of_verb(words[-1])]
                if ('I' in subjects) or ('we' in subjects) or ('We' in subjects):
                    person = 1
                elif ('you' in subjects) or ('You' in subjects):
                    person = 2
                else:
                    person = 3
                if is_plural_verb(words[-1]):
                    number = PLURAL
                else:
                    number = SINGULAR
                if (words[-2].text == 'will' and words[-2].tag_ == 'MD') or words[-2].text == 'had':
                    out.pop(-1)
                if to_tense == 'future':
                    if not (out[-1] == 'will' or out[-1] == 'be'):
                        out.append('will')
                    # handle will as a noun in future tense
                    if words[-2].text == 'will' and words[-2].tag_ == 'NN':
                        out.append('will')
                oldWord = words[-1].text
                out.append(preserve_caps(oldWord, conjugate(oldWord, tense=this_tense, person=person, number=number)))
            else:
                out.append(words[-1].text)

            # negation
            if words[-2].text + words[-1].text in ('didnot', 'donot', 'willnot', "didn't", "don't", "won't"):
                if tense == PAST:
                    out[-2] = 'did'
                elif tense == PRESENT:
                    out[-2] = 'do'
                else:
                    out.pop(-2)

            # future perfect
            if words[-1].text in ('have', 'has') and len(list(words[-1].ancestors)) and words[-1].dep_ == 'aux':
                out.pop(-1)

        text_out = ' '.join(out)

        # Remove spaces before/after punctuation:
        for char in string.punctuation:
            if char in """(<['""":
                text_out = text_out.replace(char+' ', char)
            else:
                text_out = text_out.replace(' '+char, char)

        for char in ["-", "“", "‘"]:
            text_out = text_out.replace(char+' ', char)
        for char in ["…", "”", "'s", "n't"]:
            text_out = text_out.replace(' '+char, char)

        return text_out

    def generate(self, sentence: str): 
        """
        takes in a input sentence and transforms it's tense to the target tense
        """
        perturbed_texts = self.change_tense(sentence, to_tense = random.choice(['past', 'present', 'future']) if self.to_tense == 'random' else self.to_tense)
        return [perturbed_texts]
