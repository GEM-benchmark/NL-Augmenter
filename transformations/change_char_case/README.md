# Char Case Perturbation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly changing the upper/lower cases of the letters. 

Author name: Zijian Wang (zijwang@hotmail.com)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few letters picked at random are replaced with their upper/lower cases, for example, `Chris` -> `ChriS`. This transformation will not hurt human understanding of the sentences, but could be a challenge for language models.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. 

For example, when running RoBERTa on IMDB dataset

```
python evaluate.py -t ChangeCharCase -task TEXT_CLASSIFICATION --model="aychang/roberta-base-imdb"
```

- The accuracy on a 10% subset of the IMDB sentiment dataset is 96.0
- The accuracy of the same model on the perturbed set when changing 10% chars is 91.12
- The accuracy of the same model on the perturbed set when changing 20% chars is 88.08


## What are the limitations of this transformation?
The transformation's outputs will not work with uncased models or languages without casing. 
