# Neopronoun substitution 🏳️‍⚧️


<img alt=" The neopronoun flag from the LGBTA Wiki page" title="Neopronouns Flag by Geekycorn on DeviantArt." src="https://static.wikia.nocookie.net/lgbta/images/4/47/Neopronoun_Flag.png/revision/latest/scale-to-width-down/220?cb=20200425234516" width="200" height="200" />

**1. What are neopronouns?**

Answer: _Neopronouns are a category of new (neo) pronouns that are increasingly used in place of “she,” “he,” or “they” when
referring to a person. Some examples include: xe/xem/xyr, ze/hir/hirs, and ey/em/eir. Neopronouns can be used by
anyone, though most often they are used by transgender, non-binary, and/or gender nonconforming people._
Source: https://intercultural.uncg.edu/wp-content/uploads/Neopronouns-Explained-UNCG-Intercultural-Engagement.pdf

In the image below, we can find the temporal variations in neopronoun usage over the past few years from  the **_Gender Census 2021: Worldwide Report_**.

<img title=" The neopronoun preferences over times" src="https://gendercensus.files.wordpress.com/2021/03/gc2021-pronouns-over-time-minus-he-she-they.png" width="600" height="354" />

## What type of a transformation is this?
This transformation performs **_grammatically correct substitution_** of the gendered pronouns he/she in a given sentence with their neopronoun counterparts. The reason why a simple look-up-table approach might not work as depending on the context, the _case_ can belong to the _Nominative/Subject Pronouns,	Accusative/Object Pronouns,	Pronominal Possessive/Possessive Adjectives,	Predicative Possessive/Possessive Pronouns	or Reflexive Pronouns_ categories.


Example:
```
He like himself. ↔️ Ey likes emself **OR** Ze likes zirself etc.
```
The neopronoun list is sourced from [Neopronouns-Explained resource](https://intercultural.uncg.edu/wp-content/uploads/Neopronouns-Explained-UNCG-Intercultural-Engagement.pdf) curated by UNC Greensboro and [LGBTA WIKI](https://lgbta.wikia.org/wiki/Neopronouns).
Refer to [this](https://github.com/vinayprabhu/neo_pronouns_gen) Github repo for the [dataset construction details](https://github.com/vinayprabhu/neo_pronouns_gen/blob/main/dataset_generate_neopronouns.ipynb), [examples](https://github.com/vinayprabhu/neo_pronouns_gen/blob/main/data/df_examples_neo.csv) and [pronounciation key](https://github.com/vinayprabhu/neo_pronouns_gen/blob/main/data/df_pronounce_neo.csv).

## What tasks does it intend to benefit?
As things stand, NLP models such as those deployed for neural translation fail to recognize the neopronouns and often treats them as proper nouns. For example, Google translate translates the sentence _Ve likes verself_ to ವೀ ತನ್ನನ್ನು ತಾನೇ ಇಷ್ಟಪಡುತ್ತಾನೆ into Kannada which reads _(Someone named) Vee likes himself_! Also, as revealed in this survey titled [Toward Gender-Inclusive Coreference Resolution](https://arxiv.org/pdf/1910.13913.pdf), _"Only 7.1% (one paper!) considers neopronouns and/or specific singular THEY."_
This transformation seeks to render the training data used in NLP pipelines more neopronoun aware so as to help tackle the downstream risks of [trans erasure](https://allthingslinguistic.com/post/118373603278/i-am-at-the-end-of-my-first-semester-of).


## Previous Work

_[1]_
```bibtex
@article{bertulfobeyond,
  title={Beyond He and She: A Study on the Non-Binary and Gender Neutral English Neopronouns},
  author={Bertulfo, Cherry Con-ui}
}

```

_[2]_
```bibtex
@misc{Gender_Census_2021,
author = {Cassian Lodge},
title = {Gender Census 2021: Worldwide Summary – Gender Census},
howpublished = {\url{https://gendercensus.com/results/2021-worldwide-summary/}},
month = {March},
year = {2021},
note = {(Accessed on 06/02/2021)}
}
```

_[3]_
```bibtex
@article{cao2019toward,
  title={Toward gender-inclusive coreference resolution},
  author={Cao, Yang Trista and Daum{\'e} III, Hal},
  journal={arXiv preprint arXiv:1910.13913},
  year={2019}
}

```

## What are the limitations of this

This specific pull request does not cover the  3 __Regional Nominative Pronouns__
( A , Ou and Yo) and the following  6 options in the __Other__ category of the [LGBTA WIKI](https://lgbta.wikia.org/wiki/Neopronouns)
1. It
2. One
3. Alternating Pronouns
4. No Pronouns/Pronoun Dropping
5. Nounself Pronouns
6. Emojiself Pronouns
