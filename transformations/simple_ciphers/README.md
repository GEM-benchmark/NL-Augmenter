# Simple Ciphers

This transformation modifies the input text in ways that a human could rapidly (or with
  a few minutes of work in the case of rot13) decipher, but which make the
  input sequences almost completely unlike most of the data a language model is
  likely trained on.

Author name: Jascha Sohl-Dickstein
Author email: jaschasd@google.com
Author Affiliation: Google Brain

## What type of a transformation is this?

This transformation modifies text using a variety of very simple "ciphers", that make the input sequence very dissimilar from typical input sequences:
1 - Repeat every character twice
2 - Repeat every word twice
3 - Add spaces between all characters
4 - Reverse all characters in the input string
5 - Reverse the characters in each word in the input string
6 - Reverse the order of words in the input string
7 - Replace each character with a randomly chosen Unicode homoglyph
8 - Apply the [ROT13](https://en.wikipedia.org/wiki/ROT13) substitution cipher to all Latin characters.

These transformations all change the input in ways that should be fairly easy for humans to decipher, but which will make the task far more difficult for existing language models.

## What tasks does it intend to benefit?

This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
