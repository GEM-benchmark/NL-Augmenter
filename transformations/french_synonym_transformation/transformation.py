from textblob import TextBlob, Blobber, Word
import re
from textblob_fr import PatternTagger, PatternAnalyzer
import nltk
nltk.download('wordnet')
from textblob.wordnet import NOUN, VERB, ADV, ADJ
import spacy
from spacy_lefff import LefffLemmatizer, POSTagger
from spacy.language import Language
from nltk.corpus import wordnet
import nltk
nltk.download('omw') 

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

@Language.factory('french_lemmatizer')
def create_french_lemmatizer(nlp, name):
    return LefffLemmatizer()

@Language.factory('POSTagger')
def create_POSTagger(nlp, name):
    return POSTagger()


nlp = spacy.load('fr_core_news_md')

nlp.add_pipe('POSTagger', name ='pos')
nlp.add_pipe('french_lemmatizer', name='lefff', after='pos')


def synonym_transformation(text):    
	doc = nlp(text)
	nouns = [d.text for d in doc if d.pos_ == "NOUN"]
	synonyms_noun_list = []
	for i in nouns :
		dict_noun_synonyms = {}
		dict_noun_synonyms['noun'] = i
		dict_noun_synonyms['synonyms'] = list(set([l.name() for syn in wordnet.synsets(i, lang = 'fra') for l in syn.lemmas('fra')]))
		if len(dict_noun_synonyms['synonyms']) > 0:
			synonyms_noun_list.append(dict_noun_synonyms)

	valid_noun_list = []
	for j in synonyms_noun_list:
		for k in j['synonyms']:
			valid_noun_dict = {}
			valid_noun_dict['noun'] = j['noun']
			valid_noun_dict['syn'] = k
			if nlp(j['noun']).similarity(nlp(k)) > .55 and not nlp(j['noun']).similarity(nlp(k)) >= .999:
				valid_noun_list.append(valid_noun_dict)

	text_noun_generated = []
	pertu=[]
	for l in valid_noun_list:
		text_noun_generated.append(text.replace(l['noun'], l['syn']))
	text_noun_generated.sort(reverse=True)
	for sent in text_noun_generated:
		if nlp(text).similarity(nlp(i)) > .40 and not nlp(text).similarity(nlp(i)) >= .999:
			pertu.append(sent)
			break

	return pertu




class FrenchNounSynonymTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["fr"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence : str):
        perturbed_texts = synonym_transformation(
            sentence
        )
        print("perturbed text inside of class",perturbed_texts)
        return perturbed_texts


