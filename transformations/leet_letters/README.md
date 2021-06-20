# Leet Letters 🦎 + 🎮 → 🐍
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) proportional to noise erupting 
from keyboard typos making common spelling errors.

Author name: Niklas Muennighoff (muennighoff@stu.pku.edu.cn)

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
