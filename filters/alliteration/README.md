## keywords filter

**Author: Marie Tolkiehn**\
Center for Data and Computing in Natural Sciences, Universität Hamburg\
marie.tolkiehn@desy.de

## What type of a filter is this?

This filter returns True if a sentence is an alliteration and False otherwise. 
There is an option to remove stopwords from the sentences. 

## Related Work

## What are the limitations of this filter?
There may be phonetic alliterations that are not captured by a graphematic approach. For example, `Phonetic` and `Fine` are phonetic alliterations but not graphematic ones. 
This could be ameliorated e.g. by using Carnegie Mellon's pronouncing dictionary to compare each word. 