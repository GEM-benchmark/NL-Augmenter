# Space Between Characters
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.).

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few words are picked at random and spaces are added between characters (e.g., "Marco" -> "M a r c o").

The probability of adding a space between characters can also be set (default to 1), allowing transformations like: "house" -> "h ouse" or "h o use".

Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise and readable generations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.

It could also benefit tasks involving data from OCR systems.

## What are the limitations of this transformation?
- The transformation's outputs are very simple.
- It is not capable of generating linguistically diverse text.
- This transformation will mainly affect the perfornamce of token/word-level models, while character-level models should be much more robust.