# Simple Not Substitution 🦎  + ⌨️ → 🐍
This is a sample transformation used for the purpose of demonstration. It can be used for augmenting examples for the semantic similarity task (in English).

Author name: Kaustubh Dhole
Author email: my_email@my_university.edu
Author Affiliation: My University

## What type of a transformation is this?
Given a text pair of semantically similar sentences (label 1),
this transformation generates pairs of semantically dissimilar sentences (label 0). This would be useful for training paraphrase generators as well as testing how robust they are for this simple negation. Backtranslation is used as an approximate grammatical correcter.

## What tasks does it intend to benefit?
This perturbation would benefit paraphrase detection (semantic similarity) as well as entailment tasks. For entailment tasks, it helps generates contradictory examples.

## What are the limitations of this transformation?
This is a sample transformation which makes only a single word change (only used for demonstration purpose).