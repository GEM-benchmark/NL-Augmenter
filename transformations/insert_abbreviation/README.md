# Abbreviation Replacement 🦎  + ⌨️ → 🐍
This replacement adds noise to all types of text sources (sentence, paragraph, etc.) 
according to a rule system that encodes word sequences associated with their replacement label.
As a first use case, we focus on abbreviations for both French and English.
For example:
EN : what do you think about that, it seems to be easy, no? ==> WDYT ABT that, it seems 2B EZ, no?
FR : Pourquoi tu ne viens pas? ==> pkoi tu ne V1 pô?

Author name: Caroline Brun
Author email: caroline.brun@naverlabs.com
Author Affiliation: Naver Labs Europe

Author name: Claude Roux
Author email: claude.roux@naverlabs.com
Author Affiliation: Naver Labs Europe

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness.
This perturbation replaces in texts some well known words or expressions with (one of) their abbreviations.
Most of the abbreviations covered here are quite common on social medias platforms, even though some of them are quite generic.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, machine translation etc.
This work can be quite beneficial for projects dealing with social media texts.

```python evaluate.py -t AbbreviationInsertion -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```

The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 96
The accuracy of the same model on the perturbed set = 92

## Previous Work


2) This work is partly inspired by the following work on robustness for Machine Translation:
```bibtex
@article{berard2019naver,
  title={Naver Labs Europe's Systems for the WMT19 Machine Translation Robustness Task},
  author={Berard, Alexandre and Calapodescu, Ioan and Roux, Claude},
  journal={arXiv preprint arXiv:1907.06488},
  year={2019}
}
```

## Implementation
We have specifically implemented a generic rule system in Python in order to implement these lexical rules.
These rules integrate _regular expressions_, _capsules_ (_Python functions called from within a rule_), together with _Kleene-star convention_.
(see _grammaire.py_ for a description of these rules)
   
Ex:
   1. LOL = laugh(ed) out loud
   1. NUMBER = %[0-9]+
   1. AUX = [is|was|be|have|has|had|would|will|ll]+

## What are the limitations of this transformation?

