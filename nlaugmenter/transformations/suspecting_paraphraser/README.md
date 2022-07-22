# Suspecting Paraphraser 🦎  + ⌨️ → 🐍
This paraphraser transforms a yes/no question into a ![tag question](https://www.englishclub.com/grammar/tag-questions.htm), which helps to add more question specific informality to the dataset.

Example: "Did the American National Shipment company really break its own fleet?" -> "The American National Shipment company really broke its own fleet, didn't it?"


Author name: Witold Wydmański
Author email: witold.wydmanski@uj.edu.pl
Author Affiliation: Jagiellonian University

## What type of a transformation is this?
This transformation acts like a paraphraser and makes lexical substitutions.

## What tasks does it intend to benefit?
This transformation would benefit tasks that are focused on conversational question answering.

## What are the limitations of this transformation?
The pronouns used in the endings aren't always on point - mostly because of ambiguity. As such, this transformation shouldn't be used for tasks that require their correctness.

Examples:
 - Did he drink that tea? -> He drank that tea, didn't he?
    - The pronoun gets recognized correctly
 - Has Tesla finished high school? -> Tesla has finished high school, didn't it?
    - The word Tesla gets recognized as an organization entity, thus assigned the 'it' pronoun
 - Was Sally here yesterday? -> Sally was here yesterday, wasn't [she/he/it]? (
     - Chosen at random, because any pronoun can match here. By default, names that are recognized as strongly corresponding to one of the pronouns will get 90% chance of selecting it, but it's configurable.

