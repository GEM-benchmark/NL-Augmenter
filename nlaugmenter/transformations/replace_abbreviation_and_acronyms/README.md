# Replace Abbreviations and Acronyms 🦎  + ⌨️ → 🐍
This transformation changes abbreviations and acronyms appearing in a text to their expanded form and respectively,
changes expanded abbreviations and acronyms appearing in a text to their shorter form.
E.g.: `send this file asap to human resources` might be changed to `send this file as soon as possible to HR`. As soon as possible is the expanded form of asap.

Author names:
- Maxime Meyer (maxime.meyer@vadesecure.com, Vade)
- Tatiana Ekeinhor (tatiana.ekeinhor@vadesecure.com, Vade)
- Antoine Honoré (antoine.honore@vadesecure.com, Vade)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations display high similarity to the
source sentences i.e. the code outputs highly precise generations. It is a substitution of a word or a group of words to another format that shares the exact same meaning.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Robustness Evaluation

### Text Classification

| Transformation                   | roberta-base-IMDB   |
|:---------------------------------|:--------------------|
| AbbreviationReplacement          | 96.0 -> 96.0 (0.0)  |

## Previous Work
1) This perturbation was used as part of several augmentation modules used to augment short text. It helps with diversity when combined to other perturbations such as back translation (Arxiv 2020):
```bibtex
@article{DBLP:journals/corr/abs-2007-02033,
  author    = {Mehdi Regina and
               Maxime Meyer and
               S{\'{e}}bastien Goutal},
  title     = {Text Data Augmentation: Towards better detection of spear-phishing
               emails},
  journal   = {CoRR},
  volume    = {abs/2007.02033},
  year      = {2020},
  url       = {https://arxiv.org/abs/2007.02033},
  archivePrefix = {arXiv},
  eprint    = {2007.02033},
  timestamp = {Fri, 17 Jul 2020 15:39:46 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2007-02033.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## Abbreviations and acronyms

Currently, the list of abbreviations and acronyms used in this transformation where manually gathered focusing on common abbreviations present in business communications.
Some sources are internet websites listing business abbreviations such as: https://www.themuse.com/advice/your-ultimate-cheat-sheet-to-deciphering-the-123-most-common-business-acronyms as well as abbreviations coming from documents processed at Vade.

To update or change the list of abbreviations and acronyms used, you can modify the file `abbreviations.txt`.
You can add or change abbreviations as long as you use the following format:
`Abbrevation:Expanded form` with one abbreviation per line.

The transformation can be configured to be case-sensitive.
By default, it is not the case, however this might impact the transformation when using lists of acronyms that are part of the common language.
For example: `AT` for `Anti-Tank`.
Similarly, it might impact the meaning when changing from the expanded form to the abbreviated form.
For example: `the new York stadium` for `the NY stadium`.

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation as a standalone module.
However, combined with other modules, this transformation helps to improve the understanding of the context, and generates simple but precise similar sentences (same semantic similarity).

The transformation from the expanded form to the short form might be context dependent
(this might help to improve robustness in some context, e.g.: medical context).

It is relatively easy to provide a new list of accepted acronyms and abbreviations when using the transformation (by modifying the file `abbreviations.txt`).

## Testing
You can test that everything works well by launching the test using the command below.
Make sure that you are in `transformations/replace_abbreviation_and_acronyms` and do:
```bash
$ pytest -v
```