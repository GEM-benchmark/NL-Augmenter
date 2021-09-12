# Gender Randomizer 🦎  + ⌨️ → 🐍

Author name: Tabitha Sugumar
Author email: t.sugumar@elsevier.com
Author Affiliation: Elsevier

## What type of a transformation is this?
This transformation changes names in English texts, randomizing selection so that there's an even chance of male and female names. Acknowledging that names are not deterministic identifiers of someone's gender/pronouns, here pronouns are modified to she/her/herself if the selected name is in names/female.txt and to he/his/him/himself if the selected name is in names/male.txt. These files can be modified or replaced as desired.

## What tasks does it intend to benefit?
This is intended to avoid gender bias in natural language processing models. Run this transformation on text data prior to using it to train a model.

## Previous Work
This uses the coreferee library (https://github.com/msg-systems/coreferee). The code is downloaded and included locally, to allow for slight modifications to the setup file to allow for installation in python 3.7, as required for this transformations (the coreferee library was designed/tested in python 3.8).

The names directory comes from https://www.kaggle.com/nltkdata/names. The README within the directory provides more detail.

## What are the limitations of this transformation?
This transformation does not handle gendered words such as actor/actess, waiter/waitress, etc. The handling of pronouns is limited to what the coreferee library can identify, and, in this version is limited to the segment of text fed in one iteration (ie: if a text is separated and fed in batches, the pronouns/names will not be consistent accross the text).

## Examples of this transformation

Because this is a randomized transformation, in both the selection of gender and selection of name, test examples are impossible -- the output for a single sentence is expected to be different in each successive run. Instead I've provided some example sentences and outputs for reference.

1) Input: '“Edward turned to Miss Marple. “It’s like this, you see. As Uncle Mathew grew older, he got more and more suspicious. He didn’t trust anybody.” “Very wise of him,” said Miss Marple. “The depravity of human nature is unbelievable.” '

   Possible Output: '“Edward turned to Tandie. “It’s like this, you see. As Elvira grew older, she got more and more suspicious. She didn’t trust anybody.” “Very wise of her,” said Tandie. “The depravity of human nature is unbelievable.” '

2) Input: 'I think George never tells himself the truth.'

   Possible Output: 'I think Monique never tells herself the truth.'

3) Input: 'Angela wanted to study abroad that summer but she decided to travel with her friends instead.'

   Possible Output: 'Dominique wanted to study abroad that summer but he decided to travel with his friends instead.'

4) Input: 'I thought that Michael would go to medschool, but he told me he was applying for law.'

   Possible Output: 'I thought that Arabele would go to medschool, but she told me she was applying for law.'

5) Input: 'Mattias went to New York for Christmas last year, but he wanted to stay with family for New Years.'

   Possible Output: 'Dinah went to New York for Christmas last year, but she wanted to stay with family for New Years.'


