# Random uppercase transformation
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) by randomly adding upper cased letters.

Author name: Pierre Colombo and Emile Chapuis
Author email: colombo.pierre@gmail.com and emile.chapuis@gmail.com
Author Affiliation: Telecom Paris

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few letters picked at random are replaced with uppercased letters. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
Standard technique for NLP it is similar to what is proposed in EDA.

```bibtex
@article{wei2019eda,
  title={Eda: Easy data augmentation techniques for boosting performance on text classification tasks},
  author={Wei, Jason and Zou, Kai},
  journal={arXiv preprint arXiv:1901.11196},
  year={2019}
}
```
## What are the limitations of this transformation?
The transformation's outputs are simple and could induce a huge change if the tokenizer allows uppercased, however if the tokenizer only uses lowercases it will be inefficient.