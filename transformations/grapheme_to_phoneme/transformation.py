import random
import string
import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from g2p_en import G2p


class PhonemeSubstitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, prob=0.5, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.spacy_pipeline = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.g2p = G2p()
        self.prob = prob

    def phoneme_substitution(self, text, prob=0.5, max_outputs=1):
        random.seed(self.seed)

        '''
        returns transformed sentence with words replaced with their pronunciation
        based on probability.
        '''

        doc = self.spacy_pipeline(text)

        transformed_words = []
        for token in doc:
            word = token.text
            if word in string.punctuation:
                transformed_words[-1] += word
            else:

                if random.random() < prob:
                    new_word = self.grapheme_to_phoneme(word)
                    transformed_words.append(new_word)
                else:
                    transformed_words.append(word)

        transformed_sentence = [' '.join(transformed_words)]

        return [transformed_sentence]

    def grapheme_to_phoneme(self, grapheme):
        '''
        converts each word to phonems. If there are multiple pronounciation of a
        word, only the first prononciation is taken. Stress information from each
        word is removed.
        '''

        phoenems = self.g2p(grapheme)

        if len(phoenems) > 0:
            phoenems = ''.join(phoenems)
            phoenem_without_stress = ''.join([x for x in phoenems if x.isalpha()]).lower()
            transformed_word = phoenem_without_stress
        else:
            transformed_word = grapheme

        return transformed_word

    def generate(self, sentence: str):
        perturbed = self.phoneme_substitution(
            text=sentence,
            prob=self.prob,
            max_outputs=self.max_outputs,
        )
        return perturbed
