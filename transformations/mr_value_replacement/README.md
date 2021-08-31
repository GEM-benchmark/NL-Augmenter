# MR Value Replacement 🦎  + ⌨️ → 🐍
This perturbation adds noise to a key-value meaning representation (MR) (and its corresponding sentence) by randomly substituting values/words with their synonyms (or related words).


Author name: Marco Antonio Sobrevilla Cabezudo
Author email: msobrevillac@usp.br
Author Affiliation: University of São Paulo

## What type of a transformation is this?
This transformation could augment the semantic representation of both the MR and the sentence as well as test model robustness by substituting values/words with their related words.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks on data-to-text generation.


## What are the limitations of this transformation?
The transformation uses a simple strategy to align values of a MR and tokens in the corresponding sentence. This way, there could be some problems in complex sentences. Besides, the transformation might introduce non-grammatical segments.
