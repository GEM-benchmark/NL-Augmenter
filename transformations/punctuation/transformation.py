from typing import List

from cucco import Cucco
from fastpunct import FastPunct

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class PunctuationWithRules(SentenceOperation):
    """
    This class offers method for punctuation restoration and to transform the text based on provided rules.

    Attributes:
        rules (list): List of transformation rules to be applied.
            Example: rules = ['remove_extra_white_spaces',('replace_characters', {'characters': 'are','replacement': 'TZ'}),
                   ('replace_emails', {'replacement': 'zz'})]
            Allowed rules:
                remove_accent_marks(text, excluded=None)
                remove_extra_white_spaces(text)
                remove_stop_words(self, text, ignore_case=True, language=None)
                replace_characters(self, text, characters, replacement='')
                replace_emails(text, replacement='')
                replace_emojis(text, replacement='')
                replace_hyphens(text, replacement=' ')
                replace_urls(text, replacement='')
                replace_punctuation(self, text, excluded=None, replacement='')
                replace_symbols(text,form='NFKD',excluded=None,replacement='')
    """

    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(self, seed=0, rules=None, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.fast_punct = FastPunct()
        self.normalizations = rules
        if self.normalizations:
            self.cucco = Cucco()

    def generate(self, sentence: str) -> List[str]:
        perturbed = self.fast_punct.punct(sentence)
        if self.normalizations:
            perturbed = self.cucco.normalize(perturbed, self.normalizations)
        return [perturbed]


"""
# Sample code to demonstrate.

if __name__ == '__main__':
    normalizations = ['remove_extra_white_spaces', ('replace_characters', {'characters': 'was', 'replacement': 'TZ'}),
                      ('replace_emojis', {'replacement': 'TESTO'})]
    punc = PunctuationWithRules(rules=normalizations)
    print(punc.generate('hey dude that horror   movie was   very bad.'))
"""
