# Filler Word Augmentation
This augmentation adds noise to all types of text sources (sentence, paragraph, etc.) by inserting filler
words and phrases ("ehh", "urr", "perhaps", "you know") in the text.

Author name: Venelin Kovatchev
Author email: vkovatchev@ub.edu
Author Affiliation: The University of Texas at Austin; (University of Barcelona, University of Birmingham)

## What type of a transformation is this?
This transformation tests the robustness of the systems to (coloqual) filler words and phrases.

I propose 23 different words and phrases, grouped in three categories:
- general filler words and phrases ("uhm", "err", "actually", "like", "you know"...)
- words and phrases that emphasize speaker opinion/mental state ("I think/believe/mean", "I would say"...)
- words and phrases that indicate uncertainty ("maybe", "perhaps", "probably", "possibly", "most likely")

The phrases do not modify the general meaning of the overall text, although they might introduce a slight
difference in the degree of certainty/factuality. The augmented text is very similar to the original text.

Some of these phrases have been used successfully in data augmentation before.

The transformation allows to choose which groups of words should be used.


## What tasks does it intend to benefit?
This augmentation would benefit a large variety of texts. In the first version I define them as a
SentenceOperation transformation, created for use with text classification.

However, in principle that augmentation can be used for question answering (augmenting the question),
or in text-pair tasks (augmenting both pairs in STS / NLI/ PI tasks)

Evaluation:

The accuracy of "aychang/roberta-base-imdb"
on a subset of IMDB sentiment datase = 96.0
The accuracy of the same model on the augmented set = 92.0


## Previous Work
1) "words and phrases that emphasize speaker opinion/mental state" and "words and phrases that indicate
uncertainty" have been used in augmentation experiments in my previous work and showed promising results.
In the original work they were only added at the beginning of the phrase, while this algorithm adds them
at any position.

```bibtex
@inproceedings{kovatchev-etal-2021-vectors,
    title = "Can vectors read minds better than experts? Comparing data augmentation strategies for the automated scoring of children{'}s mindreading ability",
    author = "Kovatchev, Venelin  and
      Smith, Phillip  and
      Lee, Mark  and
      Devine, Rory",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.96",
    doi = "10.18653/v1/2021.acl-long.96",
    pages = "1196--1206"}
```

2) The list of fill words is based on the work of Laserna at al. (2014). To the best of
my knowledge it has not been used for augmentation before.

```@article{doi:10.1177/0261927X14526993,
author = {Charlyn M. Laserna and Yi-Tai Seih and James W. Pennebaker},
title ={Um . . . Who Like Says You Know: Filler Word Use as a Function of Age, Gender, and Personality},
journal = {Journal of Language and Social Psychology},
volume = {33},
number = {3},
pages = {328-338},
year = {2014},
doi = {10.1177/0261927X14526993}
}
```


## What are the limitations of this transformation?
- the transformations are relatively simple

- some of the transformations affect the degree of certainty of the whole statement (e.g. by inserting
"probably", "perhaps"), which may affect the labels in some fact-based tasks. In such tasks, it is suggested
that only the "filler phrase" group is used for augmentation.
