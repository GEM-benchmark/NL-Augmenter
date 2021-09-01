# Stopword Removal
Removes stopwords from a piece of text.

## What type of a transformation is this?
By default, this simple stopword removal parses a text, removes stopwords, and returns an untokenized version of the text using nltk's toktok tokenizer and treeword bank detokenizer. All stopwords are based on nltk's library of stopwords.

## What tasks does it intend to benefit?
Removing stopwords is often one of the key steps for text-preprocessing to reduce the size of text data one has to deal with.

## What are the limitations of this transformation?
The library of stopwords are constrained by nltk's library of stopwords. Different libraries like spaCy or gensim may include or exclude certain stopwords that are inside NLTK's library of stopwords. The NLTK library is chosen simply due to its popularity compared to other libraries.

## Author
Juan Yi Loke, juanyi.loke@mail.utoronto.ca