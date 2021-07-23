# Color Transformation 🦎 → 🐍

This transformation augments the input sentence by randomly replacing colors.

Author name: Seungjae Ryan Lee
Author email: seungjaeryanlee@gmail.com

## What type of a transformation is this?

This transformation searches for colors in the input sentence. Each color is
replaced with a random color.

## What tasks does it intend to benefit?

This perturbation would benefit all tasks which have a sentence / paragraph /
document as input like text classification, text generation, etc. 

```python evaluate.py -t ColorTransformation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6") 
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of the same model on the perturbed set = 11.9221

## Data and code provenance

The color names are obtained from the 140 color names supported by modern browsers, with 7 additional
color names to allow both "gray" and "grey" variants.

The code was written from scratch by the author of this project.

## What are the limitations of this transformation?

This transformation finds color names by a simple word search, but some color
names have different semantic meaning. Therefore, words that were not intended
to describe color may be transformed. For example, "I am feeling blue" may be
transformed to "I am feeling chocolate."
