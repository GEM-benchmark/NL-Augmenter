## Token-Amount filter

Author: Robin M. Schmidt (https://scholar.google.de/citations?user=20vb63kAAAAJ&hl=de)

## What type of a filter is this?

This filter filters an example text based on a set of keywords and returns whether the supported operations are true for the input text.

Inputs:

- Array of words (e.g. ["is", "are"]), a single string is also possible
- Array of integers of elementwise required occurrences (e.g. [2, 4]), if a single integer is given same threshold is applied to all keywords
- Array of strings of comparison operations (e.g. ["<", ">"]), if a single string is given the same operation is applied to all keywords

Supported operations:
- greater than: ">"
- less than: "<"
- greater equal to: ">="
- less equal to: "<="
- equal to: "=="