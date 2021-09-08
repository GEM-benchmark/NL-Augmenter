import nltk
from nltk.corpus import wordnet
import nltk.tokenize as nt

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

''' Class that converts adjectives and adverbs to its negated antonym'''


class NegatedAntonym(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)

    def generate(self, sentence):
        return [self.Neg_Antonym(sentence)]

    def Neg_Antonym(self, sentence):

        tokenized_sent = nt.word_tokenize(sentence)
        pos_sentences = nltk.pos_tag(tokenized_sent)

        for i in range(len(pos_sentences)):
            antonyms = []
            if pos_sentences[i][1] == 'JJ' or pos_sentences[i][1] == 'JJR' or pos_sentences[i][1] == 'JJS' or \
                    pos_sentences[i][1] == 'RB' or pos_sentences[i][1] == 'RBR' or pos_sentences[i][1] == 'RBS':
                for syn in wordnet.synsets(tokenized_sent[i]):

                    for lm in syn.lemmas():

                        if lm.antonyms():
                            antonyms.append(lm.antonyms()[0].name())

                if len(antonyms) != 0:
                    tokenized_sent[i] = 'not ' + antonyms[0]

        return ' '.join(tokenized_sent)
