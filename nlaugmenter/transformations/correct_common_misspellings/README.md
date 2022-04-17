# Correct common misspellings
This perturbation corrects common misspellings in text.

Author names:
- Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)
- Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
- Sajant Anand (sajant@berkeley.edu, UC Berkeley)
- Roy Rinberg (royrinberg@gmail.com, Columbia University)

## What type of a transformation is this?
This transformation perturbs text to correct common misspellings.
It uses [this list of common misspellings](https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines) and replaces any misspelled words present in the text with their correct spelling.
In the case where a word has multiple reasonable possibilities (e.g. `imigrated->emigrated OR immigrated`), the word is left unchanged.

## What tasks does it intend to benefit?
This transformation would benefit many tasks which take in messy input (i.e. misspelled free-written text) which can be cleaned before downstream processing.

## Previous Work
There is an [existing package](https://github.com/lyda/misspell-check) which similarly checks for common misspellings.

## What are the limitations of this transformation?
This transformation is not a full-fledged spell-checker and should not be used as such; rather, it is a lightweight spell-checker which corrects only very commonly misspelled words.
It works only for English and operates only at the word-level (i.e. it does not incorporate context around individual words to gauge their spelling).

## Robustness Evaluation

Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset.
The accuracy on this subset which has 1000 examples = 96.0

1000 examples generated from 1000 original examples, with 35 successfully transformed and 965 unchanged (0.035 perturb rate).
Here is the performance of the model on the transformed set:
The accuracy on this subset which has 1000 examples = 96.0
