# French Conjugation Substitution 🦎  + ⌨️ → 🐍

This transformation change the conjugation of verbs for simple french sentences with a specified tense. It detects the pronouns used in the sentence in order to conjugate accordingly whenever a sentence contains differents verbs.


Authors : Lisa Barthe and Louanes Hamla from Fablab by Inetum in Paris

## What type of transformation it is ?
This transformation allows to create paraphrases with a different conjugation tense in french. The general meaning of the sentence remains but it can be declined on different tenses (indicative tenses for now, but subjonctive and conditional might be added on a latter version).
The sentence could be conjugated in any indicative tense, it can be transformed to the desired tense.


## Supported Task

This perturbation can be used for any French task

## What does it intend to benefit ?

This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. that requires synthetic data augmentation / diversification.

## What are the limitation of this transformation ?

The current version of this conjugation works only for indicative tenses (le présent, le passé composé, l'imparfait, le passé récent, le passé simple, le plus-que-parfait, le passé antérieur, le futur proche, le futur simple et le futur antérieur).
It only works for simple direct sentences (subject, verb, COD/COI), which contains a pronoun as subject (il, elle, je etc..),it does not detect when the subject is a couple of nouns ("les enfants" or "la jeune femme").