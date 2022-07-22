# SRL arguments exchange perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources (sentence, paragraph, etc.) proportional to number of arguments identified by model (SRL BERT).

Author name: Priyank Soni
Author email: priyank.soni@ipsoft.com
Author Affiliation: Amelia, Ipsoft

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. First we are getting semantic role labels with SRL BERT which is state of the art single model for English PropBank SRL.

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

6. if ARG0 and ARGM-PRP are both present and ARGM-PRP comes after ARG0, put ARGM-PRP just before ARG0.

Example: We will be going to the office for future meetings

[ARG0: We] [ARGM-MOD: will] be [V: going] [ARG4: to the office] [ARGM-PRP: for future meetings] . --> For future meetings, we will be going to the office.

7. if ARG0 and ARGM-CAU are both present and ARGM-CAU comes after ARG0, put ARGM-CAU just before ARG0.

Example: I am going home because it's raining.

[ARG0: I] am [V: going] [ARG4: home] [ARGM-CAU: because it 's raining] . --> Because it's raining I am going home.

8. if ARG0 and ARGM-GOL are both present and ARGM-GOL comes after ARG0, put ARGM-GOL just before ARG0.

Example: He played the match for his brother.

[ARG0: He] [V: played] [ARG1: the match] [ARGM-GOL: for his brother] . --> For his brother He played the match.

9. if ARGM-TMP and ARGM-PRP both present, exchange them.

Example: From 2023 we will be playing football for fitness.

[ARGM-TMP: From 2023] [ARG0: we] [ARGM-MOD: will] be [V: playing] [ARG1: football] [ARGM-PRP: for fitness] . --> F or fitness we will be playing football from 2023.

10 .if ARGM-TMP and ARGM-CAU both present, exchange them.

Example: In June the team will not practice because of the rain.

[ARGM-TMP: In June] [ARG0: the team] [ARGM-MOD: will] [ARGM-NEG: not] [V: practice] [ARGM-CAU: because of the rain] . --> Because of the rain the team will not practice In June.

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
3) We are referring this PropBank Annotation Guidelines document for details:
```
@article{bonial2012english,
  title={English propbank annotation guidelines},
  author={Bonial, Claire and Hwang, Jena and Bonn, Julia and Conger, Kathryn and Babko-Malaya, Olga and Palmer, Martha},
  journal={Center for Computational Language and Education Research Institute of Cognitive Science University of Colorado at Boulder},
  volume={48},
  year={2012}
}
```

4) These are 3 core propbank papers:

```@inproceedings{kingsbury2002treebank,
  title={From TreeBank to PropBank.},
  author={Kingsbury, Paul R and Palmer, Martha},
  booktitle={LREC},
  pages={1989--1993},
  year={2002},
  organization={Citeseer}
}
```
```
@article{palmer2005proposition,
  title={The proposition bank: An annotated corpus of semantic roles},
  author={Palmer, Martha and Gildea, Daniel and Kingsbury, Paul},
  journal={Computational linguistics},
  volume={31},
  number={1},
  pages={71--106},
  year={2005},
  publisher={MIT press One Rogers Street, Cambridge, MA 02142-1209, USA journals-info~…}
}
```
```
@inproceedings{gildea2002necessity,
  title={The necessity of parsing for predicate argument recognition},
  author={Gildea, Daniel and Palmer, Martha},
  booktitle={Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics},
  pages={239--246},
  year={2002}
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
