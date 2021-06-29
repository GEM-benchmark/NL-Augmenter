# Transformer Replace

This perturbation replaces words based on recommendations from a Huggingface transformer model.

Author name: Gautier Dagan
Author email: **
Author Affiliation: **

## What type of a transformation is this?

This transformation acts as a way to augment the text in way to change certain words according to some which are most likely under a transformer model.

## What tasks does it intend to benefit?

This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

`python evaluate.py -t TransformerReplace -task TEXT_CLASSIFICATION`
`model_name = "aychang/roberta-base-imdb"`

The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb")
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6")
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

## Previous Work

## What are the limitations of this transformation?

The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of generating linguistically diverse text.
