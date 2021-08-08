# Shuffle within segments
Shuffle within segments (SiS): We first split the token sequence into segments of the same label. Thus, each segment corresponds to either a mention or a sequence of out-of-mention tokens. For example, a sentence `She did not complain of headache or any other neurological symptoms .` with tags `O O O O O B-problem O B-problem I-problem I-problem I-problem O` is split into five segments: [She did not complain of], [headache], [or], [any other neurological symptoms], [.]. Then for each segment, we use a binomial distribution to randomly
decide whether it should be shuffled. If yes, the order of the tokens within the segment is shuffled while the label order is kept unchanged.

The source of the idea: https://arxiv.org/abs/2010.11683

## What type of a transformation is this?
This transformation shuffles the tokens in the sentence without breaking the sequences of the labels.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, and most importantly, a tagging task.
This would help augment data for a NER task by keeping the labels still aligned.

## What are the limitations of this transformation?
It is possible that shuffling could change the meaning of the sentence or have negative effect for NLU tasks.

## Previous Work
This perturbation is adapted from the following paper:
```
@misc{2010.11683,
Author = {Xiang Dai and Heike Adel},
Title = {An Analysis of Simple Data Augmentation for Named Entity Recognition},
Year = {2020},
Eprint = {arXiv:2010.11683},
}
```