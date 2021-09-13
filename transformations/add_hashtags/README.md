# HashTag Transformation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) 
by adding hashtags generated from sentences.

Author name: Ashish Shrivastava
Author email: ashish3586@gmail.com
Author Affiliation: Amelia Research

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. dependency nodes like 
VERB, NSUBJ, DOBJ extracted, and used for hashtag generation. Generated transformations 
display high similarity to the source sentences i.e. the code outputs highly precise 
generations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as 
input like text classification, text generation, etc. 

```python evaluate.py -t HashTagGeneration -task TEXT_CLASSIFICATION```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Hashtag 
generation using dependency nodes within the sentence boundary.
