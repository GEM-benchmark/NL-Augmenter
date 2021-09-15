# Negated Antonym Perturbation 
This perturbation rephrases the adjectives and adverbs to their negated antonym

Authors: Mayukh Das (Technical University of Braunschweig  / mayukh.das@tu-bs.de) 

## What type of a transformation is this?
This transformation detects all type of adjectives and adverb and converts them to their negated antonym.
Therfore the transformation retains the semantics of the original text as positives gets converted to negated negatives and negatives gets converted to negated positives.
Example: I think you are prepared for the test --> I think you are not unprepared for the test
## What tasks does it intend to benefit?
This can act as a valid perturbation that retains the semantics.
This will benefit for robustness of text classification like sentiment analysis, etc.


## What are the limitations of this transformation?
It is limited to only adjectives and adverbs (comparative and superlative)

## Robustness Evaluation

original accuracy: 96.0  
dataset_name: 'imdb'  
model_name: 'aychang/roberta-base-imdb'  
no_of_examples: 250  
accuracy after perturbation: 91.0  
 
The accuracy drops by 5% when tested on imdb dataset for roberta

## KeyWords
tokenizer-required  
highly-meaning-preserving	
