## Abbreviation Transformation
This transformation replaces a word or phrase with its abbreviated counterpart using a web-scraped slang dictionary.

Author Name: Gloria Wang (gwang1@imsa.edu)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness by substituting words with their abbreviations. E.g.: 'homework' -> 'hwk'.
Such abbreviations are commonly used when texting and in social media and generally doesn't affect human understanding, but may be challenging for language models.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.

## Data source
The abbreviation dictionary was scraped from https://www.noslang.com/dictionary.

## What are the limitations of this transformation?
The transformation may not be applicable in a formal context. This transformation will also be challenging for language models due to the variety of abbreviations used. Some abbreviations may also not be commonly seen as the slang dictionary has a wide variety of abbreviations.
