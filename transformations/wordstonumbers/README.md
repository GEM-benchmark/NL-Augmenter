# Words to Numbers
This transformation replaces word forms of numbers with their decimal representations, e.g. "two thousand nine hundred
and twelve" with "2912". In some sense, this is the reverse transformation of 
https://github.com/GEM-benchmark/NL-Augmenter/pull/39 and is  related to 
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

Our code is primarily loosely adapted from
https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers, though our implementation
is more general and handles sentences where only part of the sentence refers to a number.

## What are the limitations of this transformation?
- Very large numbers (>10^66) have special names that are not included here as they are likely used rarely in common
language
- The transformation does not work well with mixed-representation numbers, e.g. "140 million"
- The transformation does not work with unconventionally-formatted numbers, e.g. "one thousand million" in place of 
"one billion"
- Could handle output styled numbers, e.g. "1000000" as "1000000"
- Assumes formatting and well-formed input of number words
- While the number of people at the event was two thousand, one million people showed up to vote
- Doesn't allow for "and" like in "three hundred and twelve"