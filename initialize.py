import spacy
import random
import numpy as np

# Use this file to initialize all the heavy common packages shared by multiple transformation and filters.

# The set random seed is shared across all other imports of random and numpy
GLOBAL_SEED = 0

spacy_nlp = None

def set_seed():
    random.seed(GLOBAL_SEED)
    np.random.seed(GLOBAL_SEED)


def initialize_models():
    global spacy_nlp
    # load spacy
    spacy_nlp = spacy.load("en_core_web_sm")
