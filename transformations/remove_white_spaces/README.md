# No Space Perturbation 🦎  + ⌨️ → 🐍
This perturbation remove all white spaces to all types of text sources (sentence, paragraph, etc.)

Author name: Andreas Chandra (andreas at jakartaresearch dot com)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. All white spaces are removed from source text. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text segmentation, etc. 

```python evaluate.py -t NoSpacePerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"``p`
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6") 
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

## What are the limitations of this transformation?
The transformation's outputs are simple to be used for data augmentation. There would be no variation of this transformation like others.
