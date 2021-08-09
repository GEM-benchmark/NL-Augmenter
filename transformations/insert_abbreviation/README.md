# Abbreviation Replacement 🦎  + ⌨️ → 🐍
This replacement adds noise to all types of text sources (sentence, paragraph, etc.) 
according to a rule system that encodes word sequences associated with their replacement label.
As a first use case, we focus on abbreviations for both French and English.
For example:
EN : what do you think about that, it seems to be easy, no? ==> Wdyt abt that, it seems 2b ez, no?
FR : Pourquoi tu ne viens pas? ==> Pkoi tu ne V1 pô?

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
The transformations are applied wia two classes :  
	- AbbreviationInsertionEN for English
	- AbbreviationInsertionFR for French.
 
## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, machine translation etc.
This work can be quite beneficial for projects dealing with social media texts.

```python evaluate.py -t AbbreviationInsertionEN -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```

The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 96.0
The accuracy of the same model on the perturbed set = 91.0 (1.0 perturb rate)

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

1. The _source_ expression may have different abbreviations, but the system replace it with the first one found in the replacement rules.
This can be improved in a future version by randomly choosing an abbreviation among the possible ones.
 
2. This transformation may introduce ambiguity in the _target_ text, e.g. with replacements like:
	"bring your own beer" => "byob"
	"bring your own bottle" => "byob"
	"build your own burger" => "byob"

3. Rules for replacement are obviously non exhaustive, and may need to be enriched, for example for domain specific texts

