# Weekday Month Abbreviation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) containing names of weekdays or months.

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna

## What type of a transformation is this?
This transformation abbreviates or expands the names of months and weekdays, e.g. Mon. -> Monday.
Generated transformations display high similarity to the source sentences and does not alter the meaning and the semantic of the original texts.
It does not abbreviate plural names, e.g. Sundays.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.


## What are the limitations of this transformation?
- The transformation's outputs are very simple. It is not built to generate linguistically diverse text.
- It does not influence texts without names of weekdays or months.