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


## Previous Work

```bibtex
@article{DBLP:journals/corr/abs-1903-11508,
  author    = {Steffen Eger and
               G{\"{o}}zde G{\"{u}}l Sahin and
               Andreas R{\"{u}}ckl{\'{e}} and
               Ji{-}Ung Lee and
               Claudia Schulz and
               Mohsen Mesgar and
               Krishnkant Swarnkar and
               Edwin Simpson and
               Iryna Gurevych},
  title     = {Text Processing Like Humans Do: Visually Attacking and Shielding {NLP}
               Systems},
  journal   = {CoRR},
  volume    = {abs/1903.11508},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.11508},
  archivePrefix = {arXiv},
  eprint    = {1903.11508},
  timestamp = {Tue, 02 Apr 2019 11:16:55 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1903-11508.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```


## What are the limitations of this transformation?
- One could introduce additional leet speak transformers, which include entire words
- Some texts may be transformed into really hard to read sentences even for humans
