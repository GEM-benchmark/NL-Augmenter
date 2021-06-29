# Leet Letters 🦎 + 🎮 → 🐍
This perturbation replaces letters with leet, a common encoding used in gaming. The maximum amount of replacements in a sentence is configurable.
For example: Leet -> L33t

Author name: Niklas Muennighoff
Author email: muennighoff@stu.pku.edu.cn
Author Affiliation: Peking University

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness and visual intuition of letters. 
Transformations are chosen according to https://simple.wikipedia.org/wiki/Leet
Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. It would also benefit tasks with a relation to gaming.

```python evaluate.py -t LeetLetters -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```

## What are the limitations of this transformation?
- One could introduce additional leet speak transformers, which include entire words
- Some texts may be transformed into really hard to read sentences even for humans
