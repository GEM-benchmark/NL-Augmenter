# Noun Synonym Substitution 🦎  + ⌨️ → 🐍


This transformation change some words with synonyms according to if their POS tag is a NOUN for simple french sentences. It requires Spacy_lefff (an extention of spacy for french POS and lemmatizing) and nltk package with the open multilingual wordnet dictionary.

Authors : Lisa Barthe and Louanes Hamla from Fablab by Inetum in Paris

## What type of transformation it is ?
This transformation allows to create paraphrases with a different word in french. The general meaning of the sentence remains but it can be declined on different paraphrases with one noun variation.

## Supported Task

This perturbation can be used for any French task.

## What does it intend to benefit ?

This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. that requires synthetic data augmentation / diversification.

## What are the limitation of this transformation ?
This tool does not take the general context into account, sometimes, the ouput will not match the general sense of te sentence.