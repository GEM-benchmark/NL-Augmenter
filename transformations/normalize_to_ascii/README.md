# Normalize Text to ASCII
This transformation allows to transform text from various languages to a unified ASCII representation. The
user can choose to either replace non-ASCII characters, or to remove them entirely.

## What type of a transformation is this?
This transformation acts like a perturbation, in which all non ASCII characters are replaced by ASCII alternatives.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. In particular, this is a suitable addition for models working with languages that frequently
use non-ASCII characters.

## What are the limitations of this transformation?
While the transformation works for most European languages, it is certainly not applicable to every language. 
In particular, the transformation cannot deal with Japanese text, since text_unidecode uses Chinese transliterations 
for Kanji representations.
