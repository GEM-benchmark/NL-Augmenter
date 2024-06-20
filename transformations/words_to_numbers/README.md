# Words to Numbers
This transformation replaces word forms of numbers with their decimal representations, e.g. "two thousand nine hundred
and twelve" with "2912". In some sense, this is much harder to implement and the reverse transformation of 
https://github.com/GEM-benchmark/NL-Augmenter/pull/39 and is related to 
https://github.com/GEM-benchmark/NL-Augmenter/pull/71.

Author name: Mo Tiwari
Author email: motiwari@stanford.edu
Author Affiliation: Stanford University

## What type of  transformation is this?

This transformation functions as a perturbation to test robustness to different representations of numbers, either in
their decimal form or word form.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. and may deal with numbers written out in word form. 

## Previous Work

Several webpages exist to do this (as the code is fairly simple) but have various errors:

- https://www.browserling.com/tools/words-to-numbers cannot handle capital letters
- https://www.dcode.fr/writing-words-numbers does not provide source code

Our code is very loosely adapted from
https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers, though our implementation
is more general and handles sentences where only part of the sentence refers to a number.

This transformation is the "inverse" transformation of the 
[number-to-word transformation](https://github.com/GEM-benchmark/NL-Augmenter/blob/main/transformations/number-to-word/transformation.py)
which converts numerical representations of numbers to their word form and is a much easier transformation to implement.

## What are the limitations of this transformation?
- Very large numbers (>10^66) have special names that are not included here as they are likely used rarely in common
language
- The transformation does not work with mixed-representation numbers, e.g. "140 million"
- The transformation does not work with unconventionally-formatted numbers, e.g. "one thousand million" in place of 
"one billion", and assumes a standard formatting like "one million, three hundred thousand, seven hundred forty-two"
- The transformation may fail in settings where the actual references are ambiguous, e.g. "The numbers five hundred, forty two, and six are even"
- As an easy extension we could output styled numbers, e.g. "1000000" as "1,000,000"

## Robustness Evaluation

