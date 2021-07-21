## Speech-Tag filter

Author: Robin M. Schmidt (https://scholar.google.de/citations?user=20vb63kAAAAJ&hl=de)

## What type of a filter is this?

This filter filters an example text based on a set of speech tags and returns whether the supported operations are true for the input text.

Example Speech Tags (see spacy framework):

- NOUN
- VERB
- PROPN
- AUX
- ADP
- SYM
- NUM
- CCONJ
- DET
- PRON

Inputs:

- Array of speech tags (e.g. ["NOUN", "VERB"]), a single string is also possible
- Array of integers of elementwise required occurrences  (e.g. [2, 4]), if a single integer is given the same threshold is applied to all speech tags
- Array of strings of comparison operations (e.g. ["<", ">"]), if a single string is given the same operation is applied to all speech tags
- Optional: percentages  flag to change the occurrences  to be treated as percentages

Supported operations:

- greater than: ">"
- less than: "<"
- greater equal to: ">="
- less equal to: "<="
- equal to: "=="