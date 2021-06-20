# Whitespace Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to text by randomly removing or adding whitespace.

Author name: Xinyi Wu (email)

## What type of a transformation is this?
The transformation removes (with a probability of `remove_prob`) or adds (with a probability of `add_prob`) a whitespace at random positions.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have text as input.

```python evaluate.py -t WhitespacePerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set (`remove_prob=0.1`, `add_prob=0.05`) = 89.78

## What are the limitations of this transformation?

