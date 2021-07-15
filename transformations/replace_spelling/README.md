# Replace Spelling Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) using [corpora of misspellings](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html) making common spelling errors.

Author name: Nagender Aneja
Author email: naneja@gmail.com
Author Affiliation: Universiti Brunei Darussalam



## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few words picked at random are replaced with their common spelling errors if these words are in the [corpus of mis-spell words](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html). Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. The corpus of mis-spell words has been created by merging below four sources:

* 36,133 misspellings of 6,136 words. It is an amalgamation of errors taken from the native-speaker section (British or American writers) of the Birkbeck spelling error corpus using [Oxford Text Archive](http://ota.ahds.ac.uk/). It includes the results of spelling tests and errors from free writing, taken mostly from school children, university students or adult literacy students. Most of them were originally handwritten.
* 531 misspellings of 450 words. It is derived from one assembled by Atkinson for testing the GNU Aspell spellchecker. This version is based closely on one used by Deorowicz and Ciura in a recent paper ("Correcting spelling errors by modelling their causes"). 
* 2,455 misspellings of 1,922 words made by [Wikipedia editors](https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings).
* 1791 misspellings of 1200 target words, from the passages from the book 'English for the Rejected' by David Holbrook, Cambridge University Press, 1964. They are extracts from the writings of secondary-school children, in their next-to-last year of schooling.



## What are the limitations of this transformation?
The transformation's outputs from corpus which is mostly based on hand-written text errors. Unlike a paraphraser, it is not capable of generating linguistically diverse text.
