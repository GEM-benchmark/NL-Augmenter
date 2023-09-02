# Huggign Face Marian Machine Translator Model to load. Set of Tuples in the form: tuple=(Source-2-target languages pairs, Huggingface MarianMT Helsinki-NLP model)
HUGGINGFACE_MARIANMT_MODELS_TO_LOAD = {
    ('en2romance','Helsinki-NLP/opus-mt-en-ROMANCE'),
    ('romance2en','Helsinki-NLP/opus-mt-ROMANCE-en'),
    ('de2en','Helsinki-NLP/opus-mt-de-en'),
    ('ru2en','Helsinki-NLP/opus-mt-ru-en'),
    ('en2ar','Helsinki-NLP/opus-mt-en-ar'),
    ('en2zh','Helsinki-NLP/opus-mt-en-zh'),
    ('en2jap','Helsinki-NLP/opus-mt-en-jap'),
    ('en2ru','Helsinki-NLP/opus-mt-en-ru'),
    ('en2de','Helsinki-NLP/opus-mt-en-de'),
    ('zh2en','Helsinki-NLP/opus-mt-zh-en')
  }


EASYNMT_MODEL_NAME = 'm2m_100_418M'