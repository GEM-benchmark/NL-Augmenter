# Char Case Perturbation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly changing the upper/lower cases of the letters. 

Author name: Zijian Wang (zijwang@hotmail.com)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few letters picked at random are replaced with their upper/lower cases, for example, `Chris` -> `ChriS`. This transformation will not hurt human understanding of the sentences, but could be a challenge for language models.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. 

```
python evaluate.py -t ChangeCharCase -task TEXT_CLASSIFICATION --model="aychang/roberta-base-imdb"
```

The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a 10% subset of IMDB sentiment dataset with a 10% case changes = 95.74
The accuracy of the same model on the perturbed set = 88.26



## What are the limitations of this transformation?
The transformation's outputs will not work with uncased models or languages without casing. 
