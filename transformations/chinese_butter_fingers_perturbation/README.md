# Chinese Pinyin Butter Fingers Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese characters (sentence, paragraph, etc.) proportional to noise erupting 
from keyboard typos making errors resulting from Chinese characters that have similiar Pinyin. 

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Few Chinese characters that are picked at random will be replaced with characters 
that have similar pinyin (based on the default Pinyin keyboards in Windows and Mac OS) where the user may accidentally select the wrong character from the returned results. 

Generated transformations display high similarity to the 
source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese characters as input like text classification, 
text generation, etc.

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
