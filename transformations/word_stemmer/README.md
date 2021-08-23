# Simple Word Stemmer
This transformation applies a simple word stemming operation onto a given body of text. 

## What type of a transformation is this?
This simple word stemmer parses an input block of text and removes suffixes from each word in the block. This augmentation preserves punctuation and sentence structure.

## What tasks does it intend to benefit?
Stemming can be thought of as a normalization technique for words. It essentially converts set of words in a sentence into a sequence (in this case, back into sentence form) to shorten  lookup of certain words. Stemming is also an operation commonly use in tagging systems, indexing, SEOs, Web search results, and information retrieval. 

## What are the limitations of this transformation?
Stemming is a relatively crude heuristic that removes word suffixes with the intention of transforming words into their root forms. As a consequence, word roots may not nessecarily correspond to their true root forms -- only their prefix form. For example, "making", "makes" and "maker" being converted into "mak" instead of "make". 

## Authors
David Wang, davidw.wang@mail.utoronto.ca