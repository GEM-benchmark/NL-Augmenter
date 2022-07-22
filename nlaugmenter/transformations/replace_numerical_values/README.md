# Replace Numerical Values 🦎  + ⌨️ → 🐍
This perturbation changes the numerical values appearing in text.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations display high similarity to the
source sentences i.e. the code outputs highly precise generations.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

The accuracy of a RoBERTa model (fine-tuned on IMDB) on a subset of IMDB sentiment dataset = X
The accuracy of the same model on the perturbed set = X

The average bleu score of a distillbert model (fine-tuned on xsum) on a subset of xsum dataset = X
The average bleu score of same model on the pertubed set = X

## Previous Work
1) There has also been some recent work in the contrast sets of the GEM Benchmark (ACL 2021):
```bibtex
@article{DBLP:journals/corr/abs-2102-01672,
  title     = {The {GEM} Benchmark: Natural Language Generation, its Evaluation and
               Metrics},
  journal   = {CoRR},
  volume    = {abs/2102.01672},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.01672},
  archivePrefix = {arXiv},
  eprint    = {2102.01672},
  timestamp = {Tue, 16 Feb 2021 16:58:52 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2102-01672.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
