# Replace Abbreviations and Acronyms 🦎  + ⌨️ → 🐍
This transformation changes abbreviations and acronyms appearing in a text to their expanded form and respectively, 
changes expanded abbreviations and acronyms appearing in a text to their shorter form.
E.g.: `send this file asap to human resources` might be changed to `send this file as soon as possible to HR`. As soon as possible is the expanded form of asap.

keywords

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
```bash
$ python evaluate.py -t ReplaceAbbreviations
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
The accuracy on this subset which has 1000 examples = 96.0
Applying transformation:
100%|███████████████████████████████████████████████████████████████████████████████| 1000/1000 [06:47<00:00,  2.46it/s]
Finished transformation! 1000 examples generated from 1000 original examples, with 129 successfully transformed and 871 unchanged (0.129 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 1000 examples = 96.0
```

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

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation as a standalone module.
However, combined with other modules, this transformation helps to improve the understanding of the context, and generates simple but precise similar sentences (same semantic similarity).

The transformation from the expanded form to the short form might be context dependant 
(this might help to improve robustness in some context, e.g.: medical context).

It is relatively easy to provide a new list of accepted acronyms and abbreviations when using the transformation (by modifying the file `abbreviations.txt`).
Currently the list is relatively short and focuses on common abbreviations present in business communications.

## Testing
You can test that everything works well by launching the test using the command below.
Make sure that you are in `transformations/replace_abbreviation_and_acronyms` and do:
```bash
$ pytest -v
```