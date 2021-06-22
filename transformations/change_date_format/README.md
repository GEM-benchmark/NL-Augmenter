# Change Date Format
This perturbation changes the format of dates appearing in text.

Author name: Nivranshu Pasricha (pasricha@protonmail.com)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations paraphrase spans of text related to dates in the source sentence.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc.

## Previous Work
1) The idea is similar to contrast sets of the GEM Benchmark (ACL 2021):
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
The transformation's outputs might be too simple in some cases.