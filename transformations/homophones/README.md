# Homophones Perturbation
This perturbation replaces words with common homophones.
For example: their -> there

Author name: Mo Tiwari
Author email: motiwari@stanford.edu
Author Affiliation: Stanford University

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness against homophones, which are also common spelling mistakes. 
Transformations are chosen according to http://www.singularis.ltd.uk/bifroest/misc/homophones-list.html
Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc.

```python evaluate.py -t Homophones -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```


## Previous Work

N/A

## What are the limitations of this transformation?
- There are a finite set of homophones in the English language, so the perturbations restricted to that set
- An extension of this task could be to near-homophones or phonetically similar words
