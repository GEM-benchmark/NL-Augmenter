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
	adjectives = [d.text for d in doc if d.pos_ == "ADJ"]

	synonyms_adjective_list = []
	for i in adjectives:
		dict_adjective_synonyms = {}
		dict_adjective_synonyms['adjective'] = i
		dict_adjective_synonyms['synonyms'] = list(set([l.name() for syn in wordnet.synsets(i, lang = 'fra', pos = ADJ) for l in syn.lemmas('fra')]))
		if len(dict_adjective_synonyms['synonyms']) > 0:
			synonyms_adjective_list.append(dict_adjective_synonyms)
	
	valid_adjective_list = []
	for j in synonyms_adjective_list:
		for k in j['synonyms']:
			valid_adjective_dict = {}
			valid_adjective_dict['adjective'] = j['adjective']
			valid_adjective_dict['syn'] = k
			if nlp(j['adjective']).similarity(nlp(k)) > .50 and not nlp(j['adjective']).similarity(nlp(k)) >= .999:
				valid_adjective_list.append(valid_adjective_dict)
	text_adjective_generated = []
	for l in valid_adjective_list:
		text_adjective_generated.append(text.replace(l['adjective'], l['syn']))
	pertu=[]
	text_adjective_generated.sort()

	for i in text_adjective_generated :
		if nlp(text).similarity(nlp(i)) > .90 and not nlp(text).similarity(nlp(i)) >= .999:
			pertu.append(i)
			break

	return pertu


class FrenchAdjectivesSynonymTransformation(SentenceOperation):
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


