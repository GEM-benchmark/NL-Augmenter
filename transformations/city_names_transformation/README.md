# City Names Transformations 🦎  + ⌨️ → 🐍
This perturbation replaces instances of populous and well-known cities in a sentence with instances of less populous and less well-known cities. The code includes transformations for Spanish and English text.

Author name: Afnan Mir, Athena Wang, Nick Siegel
Author email: afnanmir@utexas.edu, wangathena68@yahoo.com, nsiegel@arlut.utexas.edu
Author Affiliation: Work completed while at the Applied Research Laboratories, The University of Texas at Austin

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. It makes lexical substitutions in sentences.

## What tasks does it intend to benefit?
This perturbation would benefit text/token classification, text-to-text generation, and other tasks that involve sentence/document input.


## Why is this transformation important?
This transformation is important for testing whether model performance on tasks that should be invariant to changes in locations listed in text are actually invariant. For example, preliminary experimentation has shown that several popular models for automatically recognizing locations via named entity recognition are not invariant to changes in location. In particular, less populous cities are more likely to be missed by named entity recognition than more populous cities even if the surrounding context is identical. This transformation was therefore created to determine whether models for other tasks exhibit similar bias.

## Installations
In order to use this transformation for Spanish, you must have the Spanish SpaCy model installed. This can be done through this [link](https://github.com/explosion/spacy-models/releases/tag/es_core_news_sm-3.1.0), or through this command:
``` sh
python -m spacy download es_core_news_sm
```

## Previous Work/References
1) World Cities Dataset https://www.kaggle.com/juanmah/world-cities

2) Assessing Demographic Bias in Named Entity Recognition:
```bibtex
@article{DBLP:journals/corr/abs-2008-03415,
  author    = {Shubhanshu Mishra and
               Sijun He and
               Luca Belli},
  title     = {Assessing Demographic Bias in Named Entity Recognition},
  journal   = {CoRR},
  volume    = {abs/2008.03415},
  year      = {2020},
  url       = {https://arxiv.org/abs/2008.03415},
  archivePrefix = {arXiv},
  eprint    = {2008.03415},
  timestamp = {Fri, 14 Aug 2020 15:14:45 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2008-03415.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```


## What are the limitations of this transformation?
The transformation's outputs may be too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of generating linguistically diverse text. 
