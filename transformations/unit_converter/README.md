# Unit converter
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.).

Author name: Marco Di Giovanni
Author email: marco.digiovanni@polimi.it
Author Affiliation: Politecnico di Milano and University of Bologna

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness.
It converts length and weight measures to different units (e.g., kilometers to miles) picking at random the new unit but converting accurately the quantity.
The transformation conserves the format of the original quantity: "100 pounds" is converted to "1600 ounces" but "one-hundred pounds" is converted to "one thousand, six hundred ounces".
Generated transformations display high similarity to the source sentences.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.


## What are the limitations of this transformation?
- This transformation could generate not fluent sentences when converting numbers with many decimal digits to words (we limit it to three decimal digits).
- It could be expanded to other quantities (such as time, e.g., converting seconds to minutes).
- It relies to spacy NER to detect QUANTITY.

## Data and code provenance

The code is fully implemented by me.

The table of conversion factors is derived from [Wikipedia](https://en.wikipedia.org/wiki/Conversion_of_units).
