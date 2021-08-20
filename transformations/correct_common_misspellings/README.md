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

## What tasks does it intend to benefit?
This transformation would benefit many tasks which take in messy input (i.e. misspelled free-written text) which can be cleaned before downstream processing.

## Previous Work
There is an [existing package](https://github.com/lyda/misspell-check) which similarly checks for common misspellings.

## What are the limitations of this transformation?
This transformation is not a full-fledged spell-checker and should not be used as such; rather, it is a lightweight spell-checker which corrects only very commonly misspelled words.