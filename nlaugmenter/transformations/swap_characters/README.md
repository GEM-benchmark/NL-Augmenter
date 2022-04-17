# Swap Characters Perturbation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly swapping any two adjacent characters with a default probability of .05. (e.g. "apple" -> "aplpe", "I like pears" -> "Il ike peasr")

Author name: Taylor Sorensen (email: tsor1313@gmail.com)

## What type of a transformation is this?
This transformation acts as a robustness to common typographical errors. Often, when typing on a keyboard, people will accidentally swap two adjacent characters. This transformation serves a check on robustness to these common human errors.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Previous Work
This has been a fairly common adversarial augmentation in NLP. It is described and explored in this paper:

```bibtex
@article{DBLP:journals/corr/abs-1901-06796,
  author    = {Wei Emma Zhang and
               Quan Z. Sheng and
               Ahoud Abdulrahmn F. Alhazmi},
  title     = {Generating Textual Adversarial Examples for Deep Learning Models:
               {A} Survey},
  journal   = {CoRR},
  volume    = {abs/1901.06796},
  year      = {2019},
  url       = {http://arxiv.org/abs/1901.06796},
  archivePrefix = {arXiv},
  eprint    = {1901.06796},
  timestamp = {Fri, 01 Feb 2019 13:39:59 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1901-06796.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
## What are the limitations of this transformation?
The transformation's outputs may occasionally change meaning or shift characters from word to word. If there is a high corruption rate, the meaning may be significantly changed or uninterpretable.
