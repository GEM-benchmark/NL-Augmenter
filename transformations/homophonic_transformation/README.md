# Homophonic transformations 🦎  + ⌨️ → 🐍
This is an example perturbation used to demonstrate how to add noise to a sentence with homophonic words .

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. 
"The world is a beautiful place ." --> "The whirled is a beautiful plaice ." 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation.

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation and has been used for demonstration. 
Unlike a paraphraser, it is not capable of generating linguistically diverse text. 