import spacy

# Use this file to initialize all the heavy common packages shared by multiple transformation and filters.

spacy_nlp = None


def initialize_models():
    global spacy_nlp
    # load spacy
    spacy_nlp = spacy.load("en_core_web_sm")
