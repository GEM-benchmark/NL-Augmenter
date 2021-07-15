# Pinyin Chinese Character Transcription 🀄  → 🅰
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) proportional to noise erupting 
from keyboard typos making common spelling errors.

Author name: Kaustubh Dhole
Author email: __
Author Affiliation: __

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few letters picked at random are replaced with letters 
which are at keyboard positions near the source letter. Generated transformations display high similarity to the 
source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

```python evaluate.py -t ButterFingersPerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6") 
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

## Previous Work

The character-to-pinyin converter at the core of this project is a neural 
model described in this paper:

```bibtex
@article{DBLP:journals/corr/abs-2004-03136,
  author    = {Kyubyong Park and
               Seanie Lee},
  title     = {g2pM: {A} Neural Grapheme-to-Phoneme Conversion Package for MandarinChinese
               Based on a New Open Benchmark Dataset},
  journal   = {CoRR},
  volume    = {abs/2004.03136},
  year      = {2020},
  url       = {https://arxiv.org/abs/2004.03136},
  archivePrefix = {arXiv},
  eprint    = {2004.03136},
  timestamp = {Wed, 08 Apr 2020 17:08:25 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2004-03136.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the limitations of this transformation?

The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
