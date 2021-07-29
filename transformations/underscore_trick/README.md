# Underscore Trick
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.).

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness.
It replaces some random spaces with underscores.
This transformation mimics particular behaviours:
- names of folders, files, classes, functions (e.g., underscore_trick)
- trick word counters when there is a limited maximum number of words to insert in an online questionary/quiz.
Generated transformations display high similarity to the source sentences.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. Especially on tasks related to understanding/generating scripts.

## What are the limitations of this transformation?
The transformation's outputs are extremely simple to be used for data augmentation.
