# Slangificator 🦎  + ⌨️ → 🐍
This transformation replaces some of the words (in particular, nouns, adjectives, and adverbs) of the original text with their corresponding slang. The replacement is done with the subset of the "Dictionary of English Slang & Colloquialisms". The amount of replacement is proportional to the corresponding probabilities of replacement.

Author name: Denis Kleyko
Author email: denis.kleyko@gmail.com
Author Affiliation: University of California, Berkeley and Research Institutes of Sweden

## What type of a transformation is this?
This transformation is intended to model slang by taking the original text and randomly replacing those words in the text, which have their slang correspondence. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Robustness Evaluation
The outcome of running 'python evaluate.py -t Slangificator' was as follows:
The accuracy on this subset which has 1000 examples = 96.0
Finished transformation! 1000 examples generated from 1000 original examples, with 999 successfully transformed and 1 unchanged (0.999 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 1000 examples = 93.0

## Previous Work
The author is not aware of the previous research work is this direction. 
The dictionaries for the parts of speech used in this transformation have been hand-crafted by the author using the "Dictionary of English Slang & Colloquialisms" (http://www.peevish.co.uk/slang/index.htm) as the only source of slang words.

## What are the limitations of this transformation?
The transformation takes into account slang collected from multiple sources, which means that there is a chance that the chosen replacements might come from different slangs say from Cockney rhyming slang and Australian Slang. 
The transformation is based on dictionaries so if the original text does not contain any of the words present in the dictionaries, the result of the transformation would correspond to the original text. 
To keep the complexity of parsing limited, the transformation makes replacements for single words only so phrases for which there are corresponding slang expressions are not transformed. 