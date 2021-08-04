# Longer Names for testing NER 🦎  + ⌨️ → 🐍
This is an example perturbation used to demonstrate how to add noise to a named-entity tagging problem.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. 
(Michael Jordan is a professor at Berkeley ., B-PER I-PER O O O O B-LOC O)
 --> (Michael Jordan is a professor at Eastern Berkeley ., B-PER I-PER O O O O B-LOC I-LOC O) 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, and most importantly a tagging task.
This would help augment data for an NER task by keeping the labels still aligned.

## What are the limitations of this transformation?
The transformation might result in different entities altogether eg. Africa is commmonly used to refer to the continent while South Africa for the country.
