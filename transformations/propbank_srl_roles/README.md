# SRL arguments exchange perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) proportional to noise erupting
from keyboard typos making common spelling errors.

Author name: Priyank Soni
Author email: priyank.soni@ipsoft.com
Author Affiliation: Amelia, Ipsoft

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. First we are getting semantic role labels with SRL BERT which is state of the art single model for English PropBank SRL.  Few letters picked at random are replaced with letters
which are at keyboard positions near the source letter. Generated transformations display high similarity to the
source sentences i.e. the code outputs highly precise generations.

Then we apply following rules to modify sentence, so that semantically they remain correct:

1. if ARGM-LOC and ARGM-TMP both present, exchange them.

 Example: Alex left for Delhi with his wife at 5 pm.

[ARG0: Alex] [V: left] [ARG2: for Delhi] [ARGM-COM: with his wife] [ARGM-TMP: at 5 pm] . --> Alex left for Delhi at 5 pm with his wife.

2. if ARG0 and ARGM-TMP both present and ARGM-TMP comes after ARG0, put ARGM-TMP just before ARG0.

 Example: John decided to join the party in December.

 [ARG0: John] decided to [V: join] [ARG1: the party] [ARGM-TMP: in December] . --> In December John decided to join the party.

3. if ARG0 and ARGM-LOC both present and ARGM-LOC comes after ARG0, put ARGM-LOC just before ARG0.

 Example: John decided to join the party in Mumbai.

 [ARG0: John] decided to [V: join] [ARG1: the party] [ARGM-LOC: in Mumbai] . --> In Mumbai John decided to join the party.

4. if ARG1 and ARGM-LOC both present and ARGM-LOC comes after ARG1, put ARGM-LOC just before ARG1.

 Example: you will absolutely love the music we will be playing in bangalore !

 you will absolutely love [ARG1: the music] [ARG0: we] [ARGM-MOD: will] be [V: playing] [ARGM-LOC: in bangalore] ! --> you will absolutely love in bangalore the music we will be playing !

5. if ARG1 and ARGM-TMP both present and ARGM-TMP comes after ARG1, put ARGM-TMP just before ARG1.

 Example: you will absolutely love the music we will be playing tomorrow !

 you will absolutely love [ARG1: the music] [ARG0: we] [ARGM-MOD: will] be [V: playing] [ARGM-TMP: tomorrow] ! --> you will absolutely love tomorrow the music we will be playing !

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.


## Previous Work
1) We are using this implementation for getting semantic roles https://demo.allennlp.org/semantic-role-labeling

2) This work is based on this paper:
```bibtex
@article{Shi2019SimpleBM,
  title={Simple BERT Models for Relation Extraction and Semantic Role Labeling},
  author={Peng Shi and Jimmy J. Lin},
  journal={ArXiv},
  year={2019},
  volume={abs/1904.05255}
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
