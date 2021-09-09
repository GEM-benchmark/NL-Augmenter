# Character Duplication
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) proportional to noise erupting from keyboard typos making common spelling errors.

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna



## What type of a transformation is this?
This transformation acts like a perturbation to test robustness.
Few letters picked at random are duplicated.
Generated transformations display high similarity to the source sentences.

## What tasks does it intend to benefit?
- This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.
- The generated texts mimic typing mistakes.

## What are the limitations of this transformation?
- This transformation is not capable of generating linguistically diverse text.
- This transformation will mainly affect the performance of token/word-level models, while character-level models should be much robust.
