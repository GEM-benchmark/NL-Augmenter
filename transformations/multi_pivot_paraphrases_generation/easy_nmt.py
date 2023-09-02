""" EasyNMT - Easy to use, state-of-the-art Neural Machine Translation - https://github.com/UKPLab/EasyNMT """
from easynmt import EasyNMT

def load_easynmt_model(model_name='m2m_100_418M'):
    """
    EasyNMT model to load
    :param model_name: name of the model to load - List of supported model visit: https://github.com/UKPLab/EasyNMT#available-models 
    :return EasyNMT Machine translation model
    """
    
    return EasyNMT(model_name)

def get_easynmt_translation(sentence,model,target_lang,source_lang=None):
    """
    Translate a sentence
    :param sentence: sentence to translate
    :param model: EasyNMT model
    :param trg: Target language for the translation
    :param source_lang: Source language for the translation. If None, determines the source languages automatically.
    :return Translated sentence 
    """
    return model.translate(sentence, source_lang=source_lang, target_lang=target_lang)