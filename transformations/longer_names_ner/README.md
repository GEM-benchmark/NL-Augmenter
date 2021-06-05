# Longer Names for testing NER 🦎  + ⌨️ → 🐍
This is an example perturbation used to demonstrate how to add noise to a named-entity tagging problem.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. 
(Neil Armstrong was the first to walk on the moon., B-PER, I-PER, O, O, O, O, O, O, O, O)
    --> (Neil D. M. Armstrong was the first to walk on the moon., B-PER, I-PER, I-PER, I-PER, O, O, O, O, O, O, O, O) 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, and most importantly a tagging task.
This would help augment data for an NER task by keeping the labels still aligned.

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation and has been used for demonstration. 
Unlike a paraphraser, it is not capable of 
generating linguistically diverse text.