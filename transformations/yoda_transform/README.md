# Yoda Transformation
This perturbation modifies sentences to flip the clauses such that it reads like "Yoda Speak". For example,
"Much to learn, you still have". This form of construction is sometimes called "XSV", where "the “X” being a stand-in
for whatever chunk of the sentence goes with the verb", and appears very rarely in English normally. For a more in-depth
description of "Yoda Speak" linguistically,
see, for example, [this article](https://www.theatlantic.com/entertainment/archive/2015/12/hmmmmm/420798/). The rarity of
this construction in ordinary language makes it particularly well suited for NL augmentation and serves as a relatively easy
but potentially powerful test of robustness.

Author names: Ryan Teehan, Vinay Prabhu, Nick Roberts, Sang Han

Author emails: rsteehan@gmail.com, vinay@unify.id, nick11roberts@cs.wisc.edu, sanghan@protonmail.com

Author Affiliations: Charles River Analytics, UnifyID, UW Madison, Independent Researcher

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Sentences with clauses transformed in this way are
comprehensible by English speakers, but may pose serious difficulty to NL algorithms. In particular, it rearranges the components
of an English sentence such that the verb comes at the end. This is rare in normal English speech but does not pose much
difficulty for English speakers.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc, but may be especially useful for robustness of POS tagging algorithms. Modifying sentence structure
in this way may expose an algorithm's reliance on spurious correlations in the training data.
## Previous Work
Our implementation of Yoda Speak borrowed from this code: https://github.com/yevbar/Yoda-Script

## Robustness Evaluation
| Dataset          | Model      | Change                                                                  |
| ------------------ | ----------- | -----------                                                                |
| SST-2 | textattack/roberta-base-SST-2 | -4% (94 -> 90%
| IMDB  | aychang/roberta-base-imdb | 0% (96 -> 96%)
| QQP | textattack/bert-base-uncased-QQP | -2% (92 -> 90%)
| MNLI | roberta-large-mnli | -3% (91 -> 88%)

## What are the limitations of this transformation?
For sentences with a number of different subjects, the performance of this perturbation may degrade or yield unexpected results.
In addition, in some instances it may remove proper noun capitalization (depending on the underlying SpaCy model) and may
add an unnecessary space between "/" separated words (ex. action/adventure).