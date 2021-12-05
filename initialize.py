import spacy
import torchtext.vocab as vocab
from spacy.tokenizer import Tokenizer
from spacy.util import (
    compile_infix_regex,
    compile_prefix_regex,
    compile_suffix_regex,
)

# Use this file to initialize all the heavy common packages shared by multiple transformation and filters.

spacy_nlp = None
glove = None


def initialize_models(model: str = "spacy", lang: str = "en"):
    """
    Initialize heavy models used across transformations/filters

    Parameter:
    ----------
    model: str, default is 'spacy'
        specify the type of model 'sapcy' or 'glove'.
    lang: str, default is 'en'
        language.

    Returns:
    --------
    None.
    """
    global spacy_nlp
    global glove

    # load spacy
    if model == "spacy":
        if lang == "en":
            spacy_nlp = spacy.load("en_core_web_sm")
        elif lang == "es":
            spacy_nlp = spacy.load("es_core_news_sm")
        elif lang == "zh":
            spacy_nlp = spacy.load("zh_core_web_sm")
        elif lang == "de":
            spacy_nlp = spacy.load("de_core_news_sm")
        elif lang == "fr":
            spacy_nlp = spacy.load("fr_core_news_sm")
    elif model == "glove":
        # load glove
        glove = vocab.GloVe(name="6B", dim="100")


def reinitialize_spacy():
    """Reinitialize global spacy tokenizer to defaults so that each
    transformation has a default spacy model to work with.
    """
    global spacy_nlp
    rules = spacy_nlp.Defaults.tokenizer_exceptions
    infix_re = compile_infix_regex(spacy_nlp.Defaults.infixes)
    prefix_re = compile_prefix_regex(spacy_nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(spacy_nlp.Defaults.suffixes)

    spacy_nlp.tokenizer = Tokenizer(
        spacy_nlp.vocab,
        rules=rules,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
    )
