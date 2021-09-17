# Sentence To Gapped Representation Transformation
This transformation is a sentence operation that converts sentences to their gapped forms, e.g.
"Paul likes coffee and Mary likes tea" -> "Paul likes coffee and Mary tea", specifically for single-predicate gaps.

Author name: Mo Tiwari
Author email: motiwari@stanford.edu
Author Affiliation: Stanford University

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness against sentences that are 
semantically equivalent but have different representation, specifically when the representations differ in gapping.

The literature in the Previous Work section describes how gapped sentences are relatively infrequent but are highly relevant
for natural language understanding (NLU) tasks. The test cases are pulled from prior work on sentence gapping.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, sentiment analysis, etc.

```python evaluate.py -t Homophones -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```

## Previous Work

- Sebastian Schuster, Joakim Nivre, and Christopher D. Manning.Sentences with Gapping: Parsing and Reconstructing Elided Predicates.,  https://arxiv.org/pdf/1804.06922.pdf
- Ray S. Jackendoff. 1971. Gapping and related rules. Linguistic Inquiry 2(1):21–35.
- John Robert Ross. 1970. Gapping and the order of constituents. In Manfred Bierwisch and Karl Erich Heidolph, editors, Progress in Linguistics, De Gruyter,
The Hague, pages 249–259.

## What are the limitations of this transformation?
- Currently, this transformation only produces single-predicate gaps; however, if a method is widely accepted for more complicated gapping, it is easy to extend this task
- The task relies on the POS tagger for cases where tenses can introduce corner cases, e.g. "He ate apples and she didn't eat pears" -> "He ate apples and she didn't pears"
- It is difficult in complex sentences to perfectly transform sentences to their "maximally gapped" forms; this is an active area of research (see Previous Work section)
- The reverse direction is also valuable and is submitted in another transformation
- Not so much a limitation, but sentences such as "Alex likes apples, oranges, and pears" can actually be seen as the gapped form of "Alex likes apples, Alex likes oranges, and Alex likes pears." As a design choice, our framework would also the explicit representation to the gapped form in this case.